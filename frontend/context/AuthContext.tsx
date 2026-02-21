"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface User {
  username: string;
  role: "user" | "admin";
}

interface AuthContextType {
  user: User | null;
  login: (username: string, role: "user" | "admin") => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(() => {
    if (typeof window === "undefined") return null;
    const saved = localStorage.getItem("cm_auth_user");
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem("cm_auth_user", JSON.stringify(user));
    } else {
      localStorage.removeItem("cm_auth_user");
    }
  }, [user]);

  const login = (username: string, role: "user" | "admin") => {
    setUser({ username, role });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, login, logout, isAuthenticated: !!user }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
