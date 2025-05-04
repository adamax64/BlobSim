import { createContext, useContext } from 'react';
import { SimDataApi, SimTime } from '../../generated';
import defaultConfig from '../default-config';
import { useMutation } from '@tanstack/react-query';

interface SimTimeContextValue {
  simTime: SimTime | undefined;
  loading: boolean;
  refreshSimTime: () => void;
}

const SimTimeContext = createContext<SimTimeContextValue | undefined>(undefined);

export const SimTimeProvider = ({ children }: { children: React.ReactNode }) => {
  const simDataApi = new SimDataApi(defaultConfig);

  const {
    data: simTime,
    isPending: loading,
    mutate: refreshSimTime,
  } = useMutation<SimTime, Error>({
    mutationFn: () => simDataApi.getSimTimeSimDataSimTimeGet(),
  });

  return <SimTimeContext.Provider value={{ simTime, loading, refreshSimTime }}>{children}</SimTimeContext.Provider>;
};

export const useSimTime = () => {
  const context = useContext(SimTimeContext);
  if (!context) {
    throw new Error('useSimTime must be used within a SimTimeProvider');
  }
  return context;
};
