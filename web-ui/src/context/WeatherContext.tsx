import { createContext, useContext, useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { SimDataApi, SeasonTemperature, WeatherInfoDto } from '../../generated';
import defaultConfig from '../default-config';

const STORAGE_KEY = 'seasonTemperature';

interface WeatherContextValue {
  weatherInfo: WeatherInfoDto | undefined;
  seasonTemperature: SeasonTemperature | undefined;
  loading: boolean;
  refreshWeatherInfo: () => void;
}

const WeatherContext = createContext<WeatherContextValue | undefined>(undefined);

const simDataApi = new SimDataApi(defaultConfig);

export const WeatherProvider = ({ children }: { children: React.ReactNode }) => {
  // Initialize from the cached value so the themed color is available immediately on load,
  // before the weather info request resolves.
  const [seasonTemperature, setSeasonTemperature] = useState<SeasonTemperature | undefined>(() => {
    if (typeof window === 'undefined') return undefined;
    return (localStorage.getItem(STORAGE_KEY) as SeasonTemperature | null) ?? undefined;
  });

  const {
    data: weatherInfo,
    isPending: loading,
    mutate: refreshWeatherInfo,
  } = useMutation<WeatherInfoDto, Error>({
    mutationFn: () => simDataApi.getWeatherInfoSimDataWeatherGet(),
  });

  useEffect(() => {
    refreshWeatherInfo();
  }, []);

  useEffect(() => {
    if (weatherInfo?.seasonTemperature) {
      setSeasonTemperature(weatherInfo.seasonTemperature);
      localStorage.setItem(STORAGE_KEY, weatherInfo.seasonTemperature);
    }
  }, [weatherInfo]);

  return (
    <WeatherContext.Provider value={{ weatherInfo, seasonTemperature, loading, refreshWeatherInfo }}>
      {children}
    </WeatherContext.Provider>
  );
};

export const useWeather = () => {
  const context = useContext(WeatherContext);
  if (!context) {
    throw new Error('useWeather must be used within a WeatherProvider');
  }
  return context;
};
