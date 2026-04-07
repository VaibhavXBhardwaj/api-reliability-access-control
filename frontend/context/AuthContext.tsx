
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { User, AuthTokens } from '../types';
import { api } from '../api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (tokens: AuthTokens) => void;
  logout: () => void;
  refresh: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const decodeToken = (token: string): User | null => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return {
      id: payload.sub || payload.id,
      email: payload.email,
      role: payload.role || 'user',
      exp: payload.exp,
    };
  } catch (e) {
    return null;
  }
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const login = useCallback((tokens: AuthTokens) => {
    localStorage.setItem('access_token', tokens.access_token);
    localStorage.setItem('refresh_token', tokens.refresh_token);
    const decoded = decodeToken(tokens.access_token);
    setUser(decoded);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    window.location.hash = '/login';
  }, []);

  const refresh = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) throw new Error('No refresh token');
    
    const response = await api.post('/v1/auth/refresh', { refresh_token: refreshToken });
    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    const decoded = decodeToken(access_token);
    setUser(decoded);
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      const decoded = decodeToken(token);
      if (decoded && decoded.exp * 1000 > Date.now()) {
        setUser(decoded);
      } else {
        // Token might be expired, attempt a silent refresh or logout
        logout();
      }
    }
    setLoading(false);
  }, [logout]);

  const value = {
    user,
    loading,
    login,
    logout,
    refresh,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
