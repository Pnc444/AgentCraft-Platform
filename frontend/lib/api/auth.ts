import { apiClient } from "./client";
import { useAuthStore } from "@/stores/authStore";
import type { User } from "@/types";

interface TokenPair {
  access: string;
  refresh: string;
}

interface RegisterResponse extends TokenPair {
  user: User;
}

export async function login(username: string, password: string): Promise<User> {
  const tokens = await apiClient<TokenPair>("/auth/token/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  useAuthStore.getState().setTokens(tokens.access, tokens.refresh);
  const user = await getMe();
  useAuthStore.getState().setUser(user);
  return user;
}

export async function register(
  username: string,
  email: string,
  password: string,
  passwordConfirm: string
): Promise<User> {
  const res = await apiClient<RegisterResponse>("/auth/register/", {
    method: "POST",
    body: JSON.stringify({
      username,
      email,
      password,
      password_confirm: passwordConfirm,
    }),
  });
  useAuthStore.getState().setTokens(res.access, res.refresh);
  useAuthStore.getState().setUser(res.user);
  return res.user;
}

export function getMe(): Promise<User> {
  return apiClient<User>("/auth/me/");
}

export async function updateProfile(data: Partial<Pick<User, "first_name" | "last_name" | "email">>): Promise<User> {
  const user = await apiClient<User>("/auth/me/", {
    method: "PATCH",
    body: JSON.stringify(data),
  });
  useAuthStore.getState().setUser(user);
  return user;
}

export function changePassword(currentPassword: string, newPassword: string): Promise<{ detail: string }> {
  return apiClient<{ detail: string }>("/auth/password/change/", {
    method: "POST",
    body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
  });
}
