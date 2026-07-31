import { Box, Zoom } from '@mui/material';
import { Dispatch, ReactNode, SetStateAction, useCallback, useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import type { EventDto } from '../../../../generated';
import { EventIntroductionStage } from './EventIntroductionStage';
import { EventStandingsStage } from './EventStandingsStage';
import { EventResultsStage } from './EventResultsStage';
import { EventControls } from './EventControls';
import { ReplayControls } from '../../replay-components/ReplayControls';

const STAGES = ['introduction', 'pre-standings', 'competition', 'results', 'post-standings'] as const;
export type EventStage = (typeof STAGES)[number];

type EventControlsConfig = {
  tick: number;
  replayTick: number;
  setReplayTick: Dispatch<SetStateAction<number>>;
  isStart: boolean;
  isEnd: boolean;
  progressButtonDisabled: boolean;
  onClickStart: () => void;
  onClickNext: () => void;
  onClickEnd: () => void;
};

type ReplayControlsConfig = {
  currentTick: number;
  maxTick: number | undefined;
  setCurrentTick: (tick: number | ((prev: number) => number)) => void;
  onGoBack: () => void;
};

type EventStagePipelineProps = {
  /** The event this pipeline presents stages for. */
  event: EventDto;
  /** Whether the event has concluded. Pass `true` for replays, which are always fully resolved. */
  isEventFinished: boolean;
  /** The interactive competition stage content (event UI table/chart). */
  competitionContent: ReactNode;
  /** Current stage index, persisted (alongside the replay tick) via `useReplayState`. */
  stageIndex: number;
  /** Setter for the current stage index. */
  setStageIndex: Dispatch<SetStateAction<number>>;
  /**
   * Live-event tick/progress controls. When provided, a single `EventControls` bar is rendered for
   * the whole pipeline, and its step back/forward buttons also walk between the introduction,
   * standings and results stages once the tick range is exhausted (as if those stages were extra
   * ticks). Omit for replays, which provide `replayControls` instead.
   */
  eventControls?: EventControlsConfig;
  /**
   * Replay tick scrubber controls. When provided, a single `ReplayControls` bar is rendered for the
   * whole pipeline, and its step back/forward buttons also walk between the introduction, standings
   * and results stages once the tick range is exhausted (as if those stages were extra ticks). Omit
   * for live events, which provide `eventControls` instead.
   */
  replayControls?: ReplayControlsConfig;
};

/**
 * Generic 5-stage presentation pipeline shared by every event type (quartered, sprint race,
 * endurance race, elimination scoring), for both the live event page and the replay page:
 * Introduction -> Standings before -> Competition -> Results -> Standings after.
 *
 * The very first render zooms the whole pipeline in; every stage change afterwards slides the
 * new stage in from the right while the previous one slides out to the left.
 */
export const EventStagePipeline = ({
  event,
  isEventFinished,
  competitionContent,
  stageIndex,
  setStageIndex,
  eventControls,
  replayControls,
}: EventStagePipelineProps) => {
  const { t } = useTranslation();
  const wasFinishedRef = useRef(isEventFinished);

  // Auto-advance to the results stage the moment a live event finishes.
  useEffect(() => {
    if (isEventFinished && !wasFinishedRef.current) {
      setStageIndex(STAGES.indexOf('results'));
    }
    wasFinishedRef.current = isEventFinished;
  }, [isEventFinished]);

  const currentStage = STAGES[stageIndex];
  const isCompetitionStage = currentStage === 'competition';
  const canStepStageBack = stageIndex > 0;
  const canStepStageForward = isCompetitionStage ? isEventFinished : stageIndex < STAGES.length - 1;

  return (
    <>
      <Box sx={{ overflow: 'hidden' }}>
        <Box
          sx={{
            display: 'flex',
            width: `${STAGES.length * 100}%`,
            transform: `translateX(-${stageIndex * (100 / STAGES.length)}%)`,
            transition: 'transform 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
          }}
        >
          <Box sx={{ width: `${100 / STAGES.length}%`, flexShrink: 0, minWidth: 0}}>
            <EventIntroductionStage
              active={currentStage === 'introduction'}
              leagueName={event.league.name}
              season={event.season}
              round={event.round}
              eventType={event.type}
            />
          </Box>
          <Box sx={{ width: `${100 / STAGES.length}%`, flexShrink: 0, minWidth: 0 }}>
            <EventStandingsStage
              active={currentStage === 'pre-standings'}
              title={t('event_stage_pipeline.pre_standings.title')}
              leagueId={event.league.id}
              leagueName={event.league.name}
              season={event.season}
              throughRound={event.round - 1}
            />
          </Box>
          <Box sx={{ width: `${100 / STAGES.length}%`, flexShrink: 0, minWidth: 0 }}>{competitionContent}</Box>
          <Box sx={{ width: `${100 / STAGES.length}%`, flexShrink: 0, minWidth: 0 }}>
            <EventResultsStage
              active={currentStage === 'results'}
              eventId={event.id}
            />
          </Box>
          <Box sx={{ width: `${100 / STAGES.length}%`, flexShrink: 0, minWidth: 0 }}>
            <EventStandingsStage
              active={currentStage === 'post-standings'}
              title={t('event_stage_pipeline.post_standings.title')}
              leagueId={event.league.id}
              leagueName={event.league.name}
              season={event.season}
              throughRound={event.round}
            />
          </Box>
        </Box>
      </Box>
      {eventControls && (
        <EventControls
          {...eventControls}
          isEventFinished={isEventFinished}
          showProgressButton={isCompetitionStage}
          isCompetitionStage={isCompetitionStage}
          canStepStageBack={canStepStageBack}
          canStepStageForward={canStepStageForward}
          onStepStageBack={() => setStageIndex((i) => Math.max(0, i - 1))}
          onStepStageForward={() => setStageIndex((i) => Math.min(STAGES.length - 1, i + 1))}
        />
      )}
      {replayControls && (
        <ReplayControls
          {...replayControls}
          isCompetitionStage={isCompetitionStage}
          canStepStageBack={canStepStageBack}
          canStepStageForward={canStepStageForward}
          onStepStageBack={() => setStageIndex((i) => Math.max(0, i - 1))}
          onStepStageForward={() => setStageIndex((i) => Math.min(STAGES.length - 1, i + 1))}
        />
      )}
    </>
  );
};

export default EventStagePipeline;

