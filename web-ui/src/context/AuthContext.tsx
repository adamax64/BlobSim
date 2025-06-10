import { createContext, useContext, useState, useEffect } from 'react';
import { AuthApi, Configuration } from '../../generated';
import defaultConfig from '../default-config';

interface AuthContextValue {
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authApi, setAuthApi] = useState(new AuthApi(defaultConfig));

  useEffect(() => {
    const token = localStorage.getItem('adminToken');
    if (token) {
      const config = new Configuration({
        basePath: defaultConfig.basePath,
        headers: { Authorization: `Bearer ${token}` },
      });

      setAuthApi(new AuthApi(config));

      // Validate the token
      authApi
        .validateTokenAuthValidateGet()
        .then(() => {
          setIsAuthenticated(true);
        })
        .catch(() => {
          // If token is invalid or expired, remove it
          localStorage.removeItem('adminToken');
          setIsAuthenticated(false);
        });
    }
  }, []);

  const login = (token: string) => {
    localStorage.setItem('adminToken', token);
    const config = new Configuration({
      basePath: defaultConfig.basePath,
      headers: { Authorization: `Bearer ${token}` },
    });
    setAuthApi(new AuthApi(config));
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('adminToken');
    setAuthApi(new AuthApi(defaultConfig));
    setIsAuthenticated(false);
  };

  return <AuthContext.Provider value={{ isAuthenticated, login, logout }}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
