import { apiClient } from "../lib/apiClient";

export interface RegisterPayload {
  email: string;
  full_name: string;
  phone?: string;
  role: "customer" | "restaurant" | "rider";
  password: string;
  password_confirm: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name: string;
  phone: string;
  role: "customer" | "restaurant" | "rider" | "admin";
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: UserProfile;
}

export const authService = {
  register: async (payload: RegisterPayload) => {
    const response = await apiClient.post("/auth/register/", payload);
    return response.data;
  },

  login: async (payload: LoginPayload): Promise<AuthResponse> => {
    const response = await apiClient.post("/auth/login/", payload);
    return response.data;
  },

  logout: async (refreshToken: string) => {
    const response = await apiClient.post("/auth/logout/", { refresh: refreshToken });
    return response.data;
  },

  verifyEmail: async (token: string) => {
    const response = await apiClient.post("/auth/verify-email/", { token });
    return response.data;
  },

  requestPasswordReset: async (email: string) => {
    const response = await apiClient.post("/auth/password-reset/request/", { email });
    return response.data;
  },

  confirmPasswordReset: async (token: string, new_password: string, new_password_confirm: string) => {
    const response = await apiClient.post("/auth/password-reset/confirm/", {
      token,
      new_password,
      new_password_confirm,
    });
    return response.data;
  },

  getMe: async (): Promise<UserProfile> => {
    const response = await apiClient.get("/auth/me/");
    return response.data.data;
  },
};
