import React, { createContext, useEffect, useState } from "react";
import api from "../api/axiosInstance.jsx";

export const AuthContext = createContext(null);

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async ({ username, password }) => {
    const { data } = await api.post("/api/auth/token/", { username, password });
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
    setUser({ username });
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUser(null);
  };

  const register = async ({ username, email, password }) => {
    await api.post("/api/auth/register/", { username, email, password });
    // auto-login after register (optional)
    await login({ username, password });
  };

  useEffect(() => {
    const access = localStorage.getItem("access");
    if (access) {
      // minimal: we only keep username in memory if we stored it earlier
      // Optional: fetch profile to get username
      setUser((u) => u || { username: "You" });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}
