import { Typography } from '@mui/material';
import { NewsDto, NewsType } from '../../../generated';
import { useTranslation } from 'react-i18next';

type NewsContentProps = {
  newsItem: NewsDto;
};

export const NewsContent = ({ newsItem }: NewsContentProps) => {
  const { t } = useTranslation();

  switch (newsItem.type) {
    case NewsType.BlobCreated:
    case NewsType.BlobTerminated:
      return (
        <Typography variant="body1">
          {t(`enums.news_type.${newsItem.type}`, { blobName: newsItem.blobName })}
        </Typography>
      );
    case NewsType.EventStarted:
    case NewsType.OngoingEvent:
      return (
        <Typography variant="body1">
          {t(`enums.news_type.${newsItem.type}`, {
            leagueName: newsItem.leagueName,
            round: newsItem.round,
            eventType: t(`enums.event_types.${newsItem.eventType}`),
          })}
        </Typography>
      );
    case NewsType.EventEnded:
      return (
        <>
          <Typography variant="body1">
            {t('enums.news_type.EVENT_ENDED.headline', { leagueName: newsItem.leagueName, round: newsItem.round })}
          </Typography>
          <ul>
            <li>
              <Typography variant="body1">
                {t('enums.news_type.EVENT_ENDED.first', { blobName: newsItem.winner })}
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                {t('enums.news_type.EVENT_ENDED.second', { blobName: newsItem.second })}
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                {t('enums.news_type.EVENT_ENDED.third', { blobName: newsItem.third })}
              </Typography>
            </li>
          </ul>
        </>
      );
    case NewsType.SeasonEnded:
      return (
        <Typography variant="body1">
          {t('enums.news_type.SEASON_ENDED', { leagueName: newsItem.leagueName, winner: newsItem.winner })}
        </Typography>
      );
    case NewsType.RookieOfTheYear:
      return (
        <Typography variant="body1">{t('enums.news_type.ROOKIE_OF_THE_YEAR', { winner: newsItem.winner })}</Typography>
      );
    case NewsType.NewSeason:
      return (
        <>
          <Typography variant="body1">{t('enums.news_type.NEW_SEASON.headline')}</Typography>
          {(newsItem.retired?.length ?? 0) > 0 && (
            <>
              <Typography variant="body1">{t('enums.news_type.NEW_SEASON.headline')}</Typography>
              <ul>{newsItem.retired?.map((name) => <li>{name}</li>)}</ul>
            </>
          )}
          {(newsItem.transfers?.length ?? 0) > 0 &&
            newsItem.transfers
              ?.filter((league) => league.blobs.length > 0)
              .map((league) => (
                <>
                  <Typography variant="body1">
                    {t('enums.news_type.NEW_SEASON.transfers', { leagueName: league.leagueName })}
                  </Typography>
                  <ul>
                    {league.blobs.map((name) => (
                      <li>{name}</li>
                    ))}
                  </ul>
                </>
              ))}
          {(newsItem.rookies?.length ?? 0) > 0 && (
            <>
              <Typography variant="body1">{t('enums.news_type.NEW_SEASON.rookies')}</Typography>
              <ul>{newsItem.rookies?.map((name) => <li>{name}</li>)}</ul>
            </>
          )}
        </>
      );
    case NewsType.NewGrandmaster:
      return (
        <Typography variant="body1">
          {t('enums.news_type.NEW_GRANDMASTER', { grandmaster: newsItem.grandmaster })}
        </Typography>
      );
    default:
      return <Typography variant="body1">{t(`enums.news_type.${newsItem.type}`)}</Typography>;
  }
};
