import { createContext, useContext, useState } from 'react';

type CurrentPageContextValue = {
  selectedMenuItem: string;
  setSelectedMenuItem: (page: string) => void;
  pageTitle?: string;
  setPageTitle: (title: string | undefined) => void;
};

const CurrentPageContext = createContext<CurrentPageContextValue | undefined>(undefined);

export const CurrentPageProvider = ({ children }: { children: React.ReactNode }) => {
  const [selectedMenuItem, setSelectedMenuItem] = useState(window.location.pathname.slice(1) || 'dashboard');
  const [pageTitle, setPageTitle] = useState<string | undefined>();

  return (
    <CurrentPageContext.Provider value={{ selectedMenuItem, setSelectedMenuItem, pageTitle, setPageTitle }}>
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
