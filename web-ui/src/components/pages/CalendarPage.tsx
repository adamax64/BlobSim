import { PageFrame } from '../common/PageFrame';
import { useMutation } from '@tanstack/react-query';
import { CalendarApi, CalendarDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { useEffect } from 'react';
import { EventCalendar } from '../calendar-components/EventCalendar';

export const CalendarPage = () => {
  const calendarApi = new CalendarApi(defaultConfig);
  const {
    data: calendar,
    mutate: loadCalendar,
    isPending: isCalendarLoading,
  } = useMutation<CalendarDto[], Error>({
    mutationFn: () => calendarApi.getSeasonCalendarCalendarGet(),
  });

  useEffect(() => {
    loadCalendar();
  }, []);

  return (
    <PageFrame showLoading={isCalendarLoading} pageName="calendar">
      <EventCalendar calendar={calendar} />
    </PageFrame>
  );
};
