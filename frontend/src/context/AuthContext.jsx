import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('lifelink_token');
    if (token) {
      authAPI.getMe()
        .then((res) => {
          setUser(res.data);
        })
        .catch(() => {
          localStorage.removeItem('lifelink_token');
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password, role) => {
    const res = await authAPI.login({ email, password, role });
    const { access_token, user_id, email: userEmail, role: userRole, profile } = res.data;
    localStorage.setItem('lifelink_token', access_token);
    setUser({ user_id, email: userEmail, role: userRole, profile });
    return res.data;
  };

  const register = async (registerData) => {
    const res = await authAPI.register(registerData);
    const { access_token, user_id, email: userEmail, role: userRole, profile } = res.data;
    localStorage.setItem('lifelink_token', access_token);
    setUser({ user_id, email: userEmail, role: userRole, profile });
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('lifelink_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
