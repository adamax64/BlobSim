from datetime import date, timedelta
from sqlalchemy.orm import Session
from domain.utils.sim_time_utils import convert_to_sim_time

from data.db.db_engine import transactional
from data.persistence.sim_data_repository import get_sim_data, save_sim_data
from domain.blob_services.blob_fetching_service import fetch_blob_by_id
from domain.dtos.mine_winners_dto import MineWinnerDto, MineWinnersDto

MINE_WINNERS_HISTORY_LIMIT = 5


def record_mine_winner(session: Session, blob_id: int, amount: int) -> None:
    """Append the current mine winner to sim_data.mine_winners and cap the history.

    The list stores the most recent winners at the end. When the list grows beyond
    MINE_WINNERS_HISTORY_LIMIT entries, the oldest entry (first element) is dropped.
    """
    sim_data = get_sim_data(session)
    winners = list(sim_data.mine_winners or [])
    winners.append({"blob_id": blob_id, "amount": amount})
    if len(winners) > MINE_WINNERS_HISTORY_LIMIT:
        winners = winners[-MINE_WINNERS_HISTORY_LIMIT:]
    sim_data.mine_winners = winners
    save_sim_data(session, sim_data)


@transactional
def get_mine_winners(session: Session) -> MineWinnersDto:
    """Fetch the mine winners history stored in sim_data.mine_winners.

    The stored list holds the most recent winners at the end. The returned list is
    reversed so the most recent winner comes first. The `date` of each entry is
    derived from the current real-world date minus the entry's index in the
    reversed list (index 0 -> today, index 1 -> yesterday, ...).
    """
    sim_data = get_sim_data(session)
    raw_winners = list(sim_data.mine_winners or [])
    reversed_winners = list(reversed(raw_winners))

    today = sim_data.sim_time
    winners: list[MineWinnerDto] = []
    for index, entry in enumerate(reversed_winners):
        blob_id = entry.get("blob_id") if isinstance(entry, dict) else None
        amount = entry.get("amount") if isinstance(entry, dict) else None
        if blob_id is None or amount is None:
            continue
        blob_dto = fetch_blob_by_id(blob_id, session)
        winners.append(
            MineWinnerDto(
                date=convert_to_sim_time(today - index - 1),
                blob=blob_dto,
                amount=amount,
            )
        )

    return MineWinnersDto(winners=winners)
