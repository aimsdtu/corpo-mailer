/**
 * Typed API functions for auth & user endpoints.
 */
import { apiFetch } from "./client";
import type { TokenResponse, User } from "@/lib/auth/store";

/* ------------------------------------------------------------------ */
/*  Auth                                                               */
/* ------------------------------------------------------------------ */

export interface RegisterPayload {
  email: string;
  password: string;
  name: string;
}

export async function register(payload: RegisterPayload) {
  return apiFetch<TokenResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function login(email: string, password: string) {
  return apiFetch<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function googleLoginRedirect() {
  // Backend returns a 302 redirect — navigate directly
  window.location.href = "/api/v1/auth/login/google";
}

export async function refresh() {
  return apiFetch<{ access_token: string; token_type: string }>("/auth/refresh", {
    method: "POST",
  });
}

export async function logout() {
  return apiFetch<void>("/auth/logout", { method: "POST" });
}

export async function me() {
  return apiFetch<{ sub: string; role: string; provider: string; email: string }>("/auth/me");
}

/* ------------------------------------------------------------------ */
/*  Users                                                              */
/* ------------------------------------------------------------------ */

export async function getUser(uuid: string) {
  return apiFetch<User>(`/users/${uuid}`);
}

export async function listUsers(params?: {
  designation?: string;
  access_level?: string;
  limit?: number;
  offset?: number;
}) {
  const qs = new URLSearchParams();
  if (params?.designation) qs.set("designation", params.designation);
  if (params?.access_level) qs.set("access_level", params.access_level);
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  const suffix = qs.toString() ? `?${qs}` : "";
  return apiFetch<User[]>(`/users${suffix}`);
}

export async function deleteUser(uuid: string) {
  return apiFetch<void>(`/users/${uuid}`, { method: "DELETE" });
}

export async function updatePassword(uuid: string, oldPassword: string, newPassword: string) {
  return apiFetch<void>(`/users/${uuid}/password`, {
    method: "PUT",
    body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
  });
}

export async function countUsers(params?: { designation?: string; access_level?: string }) {
  const qs = new URLSearchParams();
  if (params?.designation) qs.set("designation", params.designation);
  if (params?.access_level) qs.set("access_level", params.access_level);
  const suffix = qs.toString() ? `?${qs}` : "";
  return apiFetch<{ count: number }>(`/users/count${suffix}`);
}
