import { PageFrame } from '../common/PageFrame';
import { PageTitleCard } from '../common/PageTitleCard';
import { useMutation } from '@tanstack/react-query';
import { CalendarApi, CalendarDto } from '../../../generated';
import defaultConfig from '../../default-config';
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useMediaQuery, useTheme } from '@mui/material';
import { MobileCalendar } from '../calendar-components/MobileCalendar';
import { DesktopCalendar } from '../calendar-components/DesktopCalendar';

export const CalendarPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const calendarApi = new CalendarApi(defaultConfig);
  const { t } = useTranslation();
  const { data: calendar, mutate: loadCalendar } = useMutation<CalendarDto[], Error>({
    mutationFn: () => calendarApi.getSeasonCalendarCalendarGet(),
  });

  useEffect(() => {
    loadCalendar();
  }, []);

  return (
    <PageFrame>
      <PageTitleCard title={t('calendar.title')} />
      {isMobile ? <MobileCalendar calendar={calendar} /> : <DesktopCalendar calendar={calendar} />}
    </PageFrame>
  );
};
