from sqlalchemy.orm import Session

from data.db.db_engine import transactional
from data.model.blob import Blob
from data.model.league import League
from data.persistence import league_repository
from data.persistence.blob_reposiotry import save_all_blobs
from data.persistence.result_repository import get_most_recent_real_league_result_of_blob
from domain.dtos.league_dto import LeagueDto
from domain.news_services.news_service import add_new_season_news
from domain.standings_service import get_standings
from domain.utils.blob_name_utils import format_blob_name
from domain.utils.constants import CYCLES_PER_SEASON, MAX_FIELD_SIZE, MAX_LEAGUE_COUNT, MIN_FIELD_SIZE, QUEUE_LEVEL


retirees: list[str] = []
transfers: dict[League, list[str]] = {}
debuts: list[str] = []


@transactional
def get_all_real_leagues(session) -> list[LeagueDto]:
    """ Get all leagues that are not the queue. """

    leagues = league_repository.get_all_real_leagues(session)
    return [LeagueDto(id=league.id, name=league.name, field_size=len(league.players), level=league.level) for league in leagues]


@transactional
def manage_league_transfers(session: Session, current_season: int):
    """ Manage league transfers at the end of the season. """

    leagues = league_repository.get_all_leagues_ordered_by_level(session)
    transfers = {league: [] for league in leagues}

    _correct_contract_of_inactive_leagues(session, leagues)
    _retire_blobs(session, leagues, current_season)
    _manage_dropout_league(session, leagues[1:], leagues[0], current_season)
    _promote_blobs_to_leagues(session, leagues[1:], current_season)

    transfers_mapped = {league.name: names for league, names in transfers.items()}
    add_new_season_news(current_season + 1, transfers_mapped, retirees, debuts, session)


def _correct_contract_of_inactive_leagues(session, leagues: list[League]):
    for league in leagues:
        if league.level == QUEUE_LEVEL or league.players is None or len(league.players) >= 5:
            continue
        blobs: list[Blob] = league.players
        for blob in blobs:
            blob.contract += 1
        save_all_blobs(session, blobs)
        session.refresh(league)


def _promote_blobs_to_leagues(session, leagues: list[League], current_season: int):
    """ Promote blobs to the next league if they have reached the end of their contract. """

    for league_index in range(1, len(leagues)):
        league = leagues[league_index]
        next_league = leagues[league_index - 1]
        blobs: list[Blob] = _get_blobs_by_standings_order(session, league, current_season)
        for blob_index in range(_get_free_spaces(next_league)):
            if blob_index < len(blobs):
                blob = blobs[blob_index]
                blob.league_id = next_league.id
                if league.level == QUEUE_LEVEL:
                    blob.debut = current_season + 1
                    blob.contract = current_season + 3
                    debuts.append(format_blob_name(blob))
                else:
                    transfers[next_league].append(format_blob_name(blob))
        session.commit()
        session.refresh(next_league)
        session.refresh(league)
    # TODO: There may be an edge case where there may be free spaces remaining in higher leagues
    # while blobs from the queue get promoted to an empty league.
    _create_new_league_if_necessary(session, leagues, current_season)


def _create_new_league_if_necessary(session, leagues: list[League], current_season: int):
    """ Create a new league if the queue is not empty and there are not too many leagues. """

    queue = leagues[-1]
    if len(queue.players) >= MIN_FIELD_SIZE and len(leagues) < MAX_LEAGUE_COUNT + 1:
        last_league = leagues[-2]
        new_league = League(name=f'League {len(leagues)}', level=last_league.level + 1)
        new_league = league_repository.save_league(session, new_league)
        blobs: list[Blob] = _get_blobs_by_standings_order(session, queue, current_season)
        for blob_index in range(_get_free_spaces(new_league)):
            if blob_index < len(blobs):
                blob = blobs[blob_index]
                blob.league_id = new_league.id
                blob.debut = current_season + 1
                blob.contract = current_season + 3
        session.commit()


def _manage_dropout_league(session, leagues: list[League], dropout_league: League, current_season: int):
    _promote_dropout_winner_if_possibble(session, leagues, dropout_league, current_season)
    _demote_blobs_to_dropout(session, leagues, dropout_league, current_season)


def _promote_dropout_winner_if_possibble(session, leagues: list[League], dropout_league: League, current_season: int):
    dropout_winner = _get_dropout_winner(session, dropout_league, current_season)
    if dropout_winner is not None:
        leagues_by_id = {league.id: league for league in leagues}
        result_record = get_most_recent_real_league_result_of_blob(dropout_winner.id, session)
        promotee_league = leagues_by_id[int(result_record.event.league.id)]
        if len(promotee_league.players) < MAX_FIELD_SIZE or any([player.contract == current_season for player in promotee_league.players]):
            dropout_winner.league_id = promotee_league.id
            dropout_winner.contract = current_season + 3
            session.commit()
            session.refresh(dropout_league)
            session.refresh(promotee_league)
            transfers[promotee_league].append(format_blob_name(dropout_winner))


def _get_dropout_winner(session, dropout_league: League, current_season: int) -> Blob | None:
    dropouts = _get_blobs_by_standings_order(session, dropout_league, current_season)
    return dropouts[0] if len(dropouts) > 0 else None


def _demote_blobs_to_dropout(session, leagues: list[League], dropout_league: League, current_season: int):
    """ Demote blobs to the Dropout League if they have reached the end of their contract. """

    for league in leagues:
        blobs: list[Blob] = _get_blobs_by_standings_order(session, league, current_season)
        for blob in blobs:
            if blob.contract == current_season:
                if _get_free_spaces(dropout_league) > 0:
                    blob.league_id = dropout_league.id
                    blob.contract = current_season + 3

                    session.commit()
                    session.refresh(dropout_league)     # Refresh the dropout league to get the new player
                    transfers[dropout_league].append(format_blob_name(blob))
                else:
                    blob.league_id = None   # If there are no free spaces in the dropout league, retire the blob
                    retirees.append(format_blob_name(blob))

    session.commit()
    for league in leagues:
        session.refresh(league)


def _get_free_spaces(league: League):
    """ Get the number of free spaces in a league. """
    return MAX_FIELD_SIZE - len(league.players)


def _get_blobs_by_standings_order(session, league: League, current_season: int) -> list[Blob]:
    """ Get blobs in a league ordered by their standings. """

    if league.level == QUEUE_LEVEL:
        return sorted(league.players, key=lambda x: x.born)

    standings = (
        _get_most_recent_standings(session, league.id, current_season)
        if int(league.level) > 0     # we don't need older standings for Dropout league
        else get_standings(league.id, current_season, session)
    )
    if len(standings) == 0:
        if league.level == 0:
            return []
        return sorted(league.players, key=lambda x: x.born)

    standings_by_blob = {standing.blob_id: standing for standing in standings}
    return sorted(
        league.players,
        key=lambda x: standings_by_blob.get(x.id, 0).total_points if x.id in standings_by_blob else -1,
        reverse=True
    )


def _get_most_recent_standings(session, league_id: int, current_season: int):
    season = current_season
    while season > 0:
        standings = get_standings(league_id, season, session)
        if len(standings) > 0:
            return standings
        season -= 1
    return []


def _retire_blobs(session, leagues: list[League], current_season: int):
    """ Retire blobs that have reached the end of their contract or have low integrity. """

    for league in leagues:
        blobs: list[Blob] = league.players
        for blob in blobs:
            if (blob.contract == current_season and league.level == 0) or blob.integrity < CYCLES_PER_SEASON:
                blob.league_id = None
                retirees.append(format_blob_name(blob))
    session.commit()
    for league in leagues:
        session.refresh(league)
