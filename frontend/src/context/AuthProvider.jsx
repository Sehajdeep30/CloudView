import React, { createContext, useContext, useEffect, useState } from "react";
import apiClient from '../api/api.js';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkUser = async () => {
    try {
      const response = await apiClient.get("/users/me");
      setUser(response);
    } catch (error) {
      setUser(null);
      localStorage.setItem("reloadFlag", "0");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const reloadFlag = localStorage.getItem("reloadFlag");
    if (reloadFlag === "1") {
      checkUser();
    } else {
      setLoading(false);
    }
  }, []);

  const logout = async () => {
    try {
      await apiClient.post("/users/logout");
    } catch (err) {
      console.error("Logout failed:", err);
    } finally {
      localStorage.setItem("reloadFlag", "0");
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loading, checkUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);