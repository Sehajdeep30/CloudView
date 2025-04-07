import React, { createContext, useContext, useEffect, useState } from "react";
import apiClient from '../api/api.js';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const checkUser = async () => {
      try {
        const userData = await apiClient.get("/users/me");
        setUser(userData);
      } catch (error) {
        setUser(null);
      }
    };
    checkUser();
  }, []);

  const logout = async () => {
    try {
      await apiClient.post("/users/logout"); // or whatever your logout route is
    } catch (err) {
      console.error("Logout failed:", err);
    } finally {
      setUser(null);
    }
  };
  
  return (
    <AuthContext.Provider value={{ user, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
