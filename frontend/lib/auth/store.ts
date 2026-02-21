import { create } from "zustand";

export interface User {
  uuid: string;
  registered_email: string;
  name: string;
  pfp: string | null;
  access_level: string;
  metadata: Record<string, unknown>;
  oauth_provider: string | null;
  email_verified: boolean;
  is_active: boolean;
  last_login_at: string | null;
  created_at: string | null;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface AuthState {
  /** In-memory only — never persisted */
  accessToken: string | null;
  user: User | null;

  setAuth: (token: string, user: User | null) => void;
  clearAuth: () => void;
  setAccessToken: (token: string) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  user: null,

  setAuth: (token, user) => set({ accessToken: token, user }),
  clearAuth: () => set({ accessToken: null, user: null }),
  setAccessToken: (token) => set({ accessToken: token }),
}));
