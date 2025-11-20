import { createContext, useContext, useState, useEffect } from "react";
import type { AuthContextType, User } from "../types/auth";
import type { ReactNode } from "react";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [adminUser, setAdminUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const API_URL = import.meta.env.VITE_API_URL;

  //  Load user info from localStorage when app reloads
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const accessToken = localStorage.getItem("accessToken");

    if (storedUser && accessToken) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  //  Login Function (calls backend API)
  const signIn = async (email: string, password: string) => {
    try {
      const response = await fetch(`${API_URL}/admin/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        const message = errorData.error || errorData.message || "Login failed";
        throw new Error(message);
      }

      const data = await response.json();
      const { admin, accessToken, refreshToken } = data;

      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);
      localStorage.setItem("user", JSON.stringify(admin));

      setUser(admin);
      setAdminUser(admin);
    } catch (error: any) {
      console.error("Login failed:", error.message);
      throw new Error(error.message);
    }
  };

  //  Logout Function (clears tokens)
  const signOut = async () => {
    try {
      const refreshToken = localStorage.getItem("refreshToken");
      const storedUser = localStorage.getItem("user");
      const adminId = storedUser ? JSON.parse(storedUser).adminId : null;

      if (refreshToken && adminId) {
        await fetch(`${API_URL}/admin/logout/${adminId}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refreshToken })
        });
      }
    } catch (error) {
      console.error("Logout failed:", error);
    }

    // Clear all data
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");

    setUser(null);
    setAdminUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, adminUser, loading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
