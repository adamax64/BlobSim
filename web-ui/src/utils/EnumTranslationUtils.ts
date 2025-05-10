import { EventType } from '../../generated';

export function translateEventType(eventType: EventType): string {
  switch (eventType) {
    case EventType.QuarteredOneShotScoring:
      return 'Quartered One Shot High Jump';
    case EventType.QuarteredTwoShotScoring:
      return 'Quartered Two Shot High Jump';
    case EventType.EnduranceRace:
      return 'Endurance Race';
    default:
      return 'Unknown Event Type';
  }
}
