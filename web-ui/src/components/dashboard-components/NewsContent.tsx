import { Typography, Box, Link } from '@mui/material';
import { NewsDto, NewsType } from '../../../generated';
import { useTranslation } from 'react-i18next';
import { useState } from 'react';
import { IconNameWithDetailsModal } from '../common/IconNameWithDetailsModal';
import { InlineTranslatedBlob } from '../../components/common/InlineTranslatedBlob';
import ResultsModal from '../event-components/ResultsModal';

type NewsContentProps = {
  newsItem: NewsDto;
};

export const NewsContent = ({ newsItem }: NewsContentProps) => {
  const { t } = useTranslation();
  const [resultsOpen, setResultsOpen] = useState(false);
  const [resultsEventId, setResultsEventId] = useState<number | null>(null);

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
          <Link
            href="#"
            variant="body1"
            onClick={(e) => {
              e.preventDefault();
              const eid = newsItem.eventId ?? null;
              if (eid == null) {
                // nothing to open
                // eslint-disable-next-line no-console
                console.warn('News item has no eventId');
                return;
              }
              setResultsEventId(eid);
              setResultsOpen(true);
            }}
          >
            {t('enums.news_type.EVENT_ENDED.results')}
          </Link>
          <ResultsModal eventId={resultsEventId} open={resultsOpen} onClose={() => setResultsOpen(false)} />
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
