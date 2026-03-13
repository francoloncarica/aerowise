import { createContext, useContext, useState, useEffect } from 'react';
import { panelCheck } from '../api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('panel_token'));
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    if (token) {
      panelCheck(token)
        .then(() => {
          setIsAuthenticated(true);
        })
        .catch(() => {
          setToken(null);
          localStorage.removeItem('panel_token');
          setIsAuthenticated(false);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem('panel_token', newToken);
    setIsAuthenticated(true);
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('panel_token');
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout, isAuthenticated, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

export default AuthContext;
