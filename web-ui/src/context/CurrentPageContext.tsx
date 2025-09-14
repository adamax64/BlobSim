import { createContext, useContext, useState } from 'react';
import { AppPage } from '../components/root-components/constants';

type CurrentPageContextValue = {
  currentPage: AppPage;
  setCurrentPage: (page: AppPage) => void;
  pageTitle?: string;
  setPageTitle: (title: string | undefined) => void;
};

const CurrentPageContext = createContext<CurrentPageContextValue | undefined>(undefined);

export const CurrentPageProvider = ({ children }: { children: React.ReactNode }) => {
  const [currentPage, setCurrentPage] = useState<AppPage>(
    (window.location.pathname.slice(1) as AppPage) || 'dashboard',
  );
  const [pageTitle, setPageTitle] = useState<string | undefined>();

  return (
    <CurrentPageContext.Provider value={{ currentPage, setCurrentPage, pageTitle, setPageTitle }}>
      {children}
    </CurrentPageContext.Provider>
  );
};

export const useCurrentPage = () => {
  const context = useContext(CurrentPageContext);
  if (!context) {
    throw new Error('useCurrentPage must be used within a CurrentPageProvider');
  }
  return context;
};
