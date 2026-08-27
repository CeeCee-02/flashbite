import { create } from "zustand";
import { UserProfile, authService } from "../services/auth";

interface AuthState {
  user: UserProfile | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  setAuth: (user: UserProfile, access: string, refresh: string) => void;
  logout: () => Promise<void>;
  initAuth: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,

  setAuth: (user, access, refresh) => {
    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    set({
      user,
      accessToken: access,
      refreshToken: refresh,
      isAuthenticated: true,
    });
  },

  logout: async () => {
    const refresh = get().refreshToken;
    if (refresh) {
      try {
        await authService.logout(refresh);
      } catch (err) {
        console.error("Logout API call error:", err);
      }
    }
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    });
  },

  initAuth: () => {
    if (typeof window !== "undefined") {
      const userStr = localStorage.getItem("user");
      const access = localStorage.getItem("access_token");
      const refresh = localStorage.getItem("refresh_token");

      if (userStr && access && refresh) {
        try {
          const user = JSON.parse(userStr);
          set({
            user,
            accessToken: access,
            refreshToken: refresh,
            isAuthenticated: true,
          });
        } catch (e) {
          localStorage.removeItem("user");
        }
      }
    }
  },
}));
