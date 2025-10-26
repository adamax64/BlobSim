import { Typography, Box } from '@mui/material';
import { NewsDto, NewsType } from '../../../generated';
import { useTranslation } from 'react-i18next';
import { IconNameWithDetailsModal } from '../common/IconNameWithDetailsModal';
import { InlineTranslatedBlob } from '../../components/common/InlineTranslatedBlob';

type NewsContentProps = {
  newsItem: NewsDto;
};

export const NewsContent = ({ newsItem }: NewsContentProps) => {
  const { t } = useTranslation();

  switch (newsItem.type) {
    case NewsType.BlobCreated:
    case NewsType.BlobTerminated:
      return (
        <InlineTranslatedBlob
          translationKey={`enums.news_type.${newsItem.type}`}
          blob={newsItem.blob ?? undefined}
          interpolationKey="blobName"
        />
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
            <li className="flex">
              <Typography variant="body1">{t('enums.news_type.EVENT_ENDED.first')}</Typography>
              {newsItem.winner && (
                <Box component="span" display="inline-flex" alignItems="center" ml={1}>
                  <IconNameWithDetailsModal
                    blob={newsItem.winner}
                    name={newsItem.winner.name}
                    color={newsItem.winner.color}
                    atRisk={newsItem.winner.atRisk}
                    isRookie={newsItem.winner.isRookie}
                  />
                </Box>
              )}
            </li>
            <li className="flex">
              <Typography variant="body1">{t('enums.news_type.EVENT_ENDED.second')}</Typography>
              {newsItem.second && (
                <Box component="span" display="inline-flex" alignItems="center" ml={1}>
                  <IconNameWithDetailsModal
                    blob={newsItem.second ?? undefined}
                    name={newsItem.second?.name ?? ''}
                    color={newsItem.second?.color ?? '#888888'}
                    atRisk={newsItem.second?.atRisk}
                    isRookie={newsItem.second?.isRookie}
                  />
                </Box>
              )}
            </li>
            <li className="flex">
              <Typography variant="body1">{t('enums.news_type.EVENT_ENDED.third')}</Typography>
              {(newsItem.third as any) && (
                <Box component="span" display="inline-flex" alignItems="center" ml={1}>
                  <IconNameWithDetailsModal
                    blob={newsItem.third ?? undefined}
                    name={newsItem.third?.name ?? ''}
                    color={newsItem.third?.color ?? '#888888'}
                    atRisk={newsItem.third?.atRisk}
                    isRookie={newsItem.third?.isRookie}
                  />
                </Box>
              )}
            </li>
          </ul>
        </>
      );
    case NewsType.SeasonEnded:
      return (
        <InlineTranslatedBlob
          translationKey={`enums.news_type.SEASON_ENDED`}
          blob={newsItem.winner ?? undefined}
          interpolationKey="winner"
          otherInterpolations={{ leagueName: newsItem.leagueName ?? '' }}
        />
      );
    case NewsType.RookieOfTheYear:
      return (
        <InlineTranslatedBlob
          translationKey={`enums.news_type.ROOKIE_OF_THE_YEAR`}
          blob={newsItem.winner ?? undefined}
          interpolationKey="winner"
        />
      );
    case NewsType.NewSeason:
      return (
        <>
          <Typography variant="body1">
            {t('enums.news_type.NEW_SEASON.headline', { season: newsItem.season })}
          </Typography>
          {(newsItem.retired?.length ?? 0) > 0 && (
            <>
              <Typography variant="body1">{t('enums.news_type.NEW_SEASON.headline')}</Typography>
              <ul>
                {(newsItem.retired as any[])?.map((b) => (
                  <li key={b.id}>
                    <IconNameWithDetailsModal blob={b} blobId={b.id} name={b.name} color={b.color} />
                  </li>
                ))}
              </ul>
            </>
          )}
          {(newsItem.transfers?.length ?? 0) > 0 &&
            newsItem.transfers
              ?.filter((league) => league.blobs.length > 0)
              .map((league) => (
                <Box key={league.leagueName}>
                  <Typography variant="body1">
                    {t('enums.news_type.NEW_SEASON.transfers', { leagueName: league.leagueName })}
                  </Typography>
                  <ul>
                    {(league.blobs as any[]).map((b) => (
                      <li key={b.id}>
                        <IconNameWithDetailsModal blob={b} blobId={b.id} name={b.name} color={b.color} />
                      </li>
                    ))}
                  </ul>
                </Box>
              ))}
          {(newsItem.rookies?.length ?? 0) > 0 && (
            <>
              <Typography variant="body1">{t('enums.news_type.NEW_SEASON.rookies')}</Typography>
              <ul>
                {(newsItem.rookies as any[])?.map((b) => (
                  <li key={b.id}>
                    <IconNameWithDetailsModal blob={b} blobId={b.id} name={b.name} color={b.color} />
                  </li>
                ))}
              </ul>
            </>
          )}
        </>
      );
    case NewsType.NewGrandmaster:
      return (
        <InlineTranslatedBlob
          translationKey={`enums.news_type.NEW_GRANDMASTER`}
          blob={newsItem.grandmaster ?? undefined}
          interpolationKey="grandmaster"
        />
      );
    default:
      return <Typography variant="body1">{t(`enums.news_type.${newsItem.type}`)}</Typography>;
  }
};
