import { JSX, useEffect } from 'react';
import SevereColdIcon from '@mui/icons-material/SevereCold';
import HeatIcon from '../icons/weather-icons/Heat';
import { useMutation } from '@tanstack/react-query';
import { Box, Card, CardContent, SvgIconProps, Typography } from '@mui/material';
import RainyIcon from '../icons/weather-icons/Rainy';
import SunnyCloudyIcon from '../icons/weather-icons/SunnyCloudy';
import SunnyRainyIcon from '../icons/weather-icons/SunnyRainy';
import HeavyRainIcon from '../icons/weather-icons/HeavyRain';
import { useTranslation } from 'react-i18next';
import type { SvgIconComponent } from '@mui/icons-material';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import CloudIcon from '@mui/icons-material/Cloud';
import ThunderstormIcon from '@mui/icons-material/Thunderstorm';
import CloudySnowingIcon from '@mui/icons-material/CloudySnowing';
import FoggyIcon from '@mui/icons-material/Foggy';
import { SimDataApi, WeatherInfoDto, WeatherType } from '../../../generated';
import defaultConfig from '../../default-config';
import { useIsMobile } from '../../hooks/useIsMobile';
import DynamicTooltip from '../common/DynamicTooltip';
import { EfficiencyMeter } from '../common/EfficiencyMeter';

const WEATHER_ICONS: Record<WeatherType, SvgIconComponent | ((props: SvgIconProps) => JSX.Element)> = {
  [WeatherType.Sunny]: WbSunnyIcon,
  [WeatherType.SunnyCloudy]: SunnyCloudyIcon,
  [WeatherType.Cloudy]: CloudIcon,
  [WeatherType.SunnyRain]: SunnyRainyIcon,
  [WeatherType.Rain]: RainyIcon,
  [WeatherType.HeavyRain]: HeavyRainIcon,
  [WeatherType.Storm]: ThunderstormIcon,
  [WeatherType.Heat]: HeatIcon,
  [WeatherType.Snowy]: CloudySnowingIcon,
  [WeatherType.Freezy]: SevereColdIcon,
  [WeatherType.Foggy]: FoggyIcon,
};

const simDataApi = new SimDataApi(defaultConfig);

export default function WeatherCard() {
  const { t } = useTranslation();
  const isMobile = useIsMobile();

  const { data: weatherInfo, mutate: fetchWeatherInfo } = useMutation<WeatherInfoDto, Error>({
    mutationFn: () => simDataApi.getWeatherInfoSimDataWeatherGet(),
  });

  useEffect(() => {
    fetchWeatherInfo();
  }, []);

  const weatherType = weatherInfo?.weather;
  const WeatherIcon = weatherType ? WEATHER_ICONS[weatherType] : undefined;
  const weatherName = weatherType ? t(`weather.types.${weatherType}`) : '';
  const windLabel = t('weather.wind');

  return (
    <Card>
      <CardContent sx={{pb: '16px !important'}}>
        <Box display="flex" flexDirection="column" height="100%">
          <Typography variant="h6">{t('weather.title')}</Typography>
          <Box display="flex" alignItems="center" justifyContent="space-around" gap={{ xs: 1, sm: 5}} height="100%" paddingX={{ xs: 0, sm: 1.5 }}>
            <DynamicTooltip title={isMobile && weatherName}>
              <Box display="flex" flexDirection="column" alignItems="center" gap={0.5} height="100%">
                {WeatherIcon && <WeatherIcon sx={{ fontSize: 48, m: '14px' }} />}
                {!isMobile && <Typography variant="body2">{weatherName}</Typography>}
              </Box>
            </DynamicTooltip>
            <DynamicTooltip title={isMobile && windLabel}>
              <Box>
                <EfficiencyMeter label={isMobile ? undefined : windLabel} value={weatherInfo?.wind ?? 0} size={76} />
              </Box>
            </DynamicTooltip>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
