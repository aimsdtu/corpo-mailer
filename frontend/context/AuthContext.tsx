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
  isInitialized: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    // Read from localStorage only after hydration is complete
    const saved = localStorage.getItem("cm_auth_user");
    if (saved) {
      try {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setUser(JSON.parse(saved));
            } catch (e) {
        console.error("Failed to parse auth user", e);
      }
    }
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setIsInitialized(true);
  }, []);

  useEffect(() => {
    if (!isInitialized) return; // Don't wipe on first render if empty
    if (user) {
      localStorage.setItem("cm_auth_user", JSON.stringify(user));
    } else {
      localStorage.removeItem("cm_auth_user");
    }
  }, [user, isInitialized]);

  const login = (username: string, role: "user" | "admin") => {
    setUser({ username, role });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, login, logout, isAuthenticated: !!user, isInitialized }}
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
