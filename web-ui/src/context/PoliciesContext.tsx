import { createContext, Dispatch, SetStateAction, useContext } from 'react';
import { PoliciesApi, PolicyDto } from '../../generated';
import defaultConfig from '../default-config';
import { useMutation } from '@tanstack/react-query';

interface PolicyContextValue {
  policiesLoading: boolean;
  policies: PolicyDto[] | undefined;
  refreshPolicies: () => void;
}

export const PoliciesContext = createContext<PolicyContextValue | undefined>(undefined);

export const PoliciesProvider = ({ children }: { children: React.ReactNode }) => {
  const policiesApi = new PoliciesApi(defaultConfig);

  const { data, isPending, mutate } = useMutation<PolicyDto[], Error>({
    mutationFn: () => policiesApi.getActivePoliciesPoliciesGet(),
  });

  return (
    <PoliciesContext.Provider value={{ policiesLoading: isPending, policies: data, refreshPolicies: mutate }}>
      {children}
    </PoliciesContext.Provider>
  );
};

export const usePolicies = () => {
  const context = useContext(PoliciesContext);
  if (!context) {
    throw new Error('usePoli must be used within a PoliciesProvider');
  }
  return context;
};
