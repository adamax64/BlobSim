import { createContext, use } from 'react';
import { SimDataApi, SimTimeDto } from '../../generated';
import defaultConfig from '../default-config';
import { useMutation } from '@tanstack/react-query';

interface SimTimeContextValue {
  simTime: SimTimeDto | undefined;
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
  } = useMutation<SimTimeDto, Error>({
    mutationFn: () => simDataApi.getSimTimeSimDataSimTimeGet(),
  });

  return <SimTimeContext value={{ simTime, loading, refreshSimTime }}>{children}</SimTimeContext>;
};

export const useSimTime = () => {
  const context = use(SimTimeContext as React.Context<SimTimeContextValue>);
  return context;
};
