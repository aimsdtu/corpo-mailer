/**
 * apiFetch — thin wrapper around fetch that:
 *  1. Attaches the in-memory access token as Bearer header.
 *  2. On 401, attempts a single /auth/refresh call, retries the original request.
 *  3. Serialises refresh calls so only one is in-flight at a time.
 */
import { useAuthStore } from "@/lib/auth/store";
import { broadcastLogout } from "@/lib/auth/sync";

const BASE = "/api/v1";

let refreshPromise: Promise<string | null> | null = null;

async function refreshAccessToken(): Promise<string | null> {
  const res = await fetch(`${BASE}/auth/refresh`, {
    method: "POST",
    credentials: "include", // sends httpOnly cookie
  });
  if (!res.ok) return null;
  const body = await res.json();
  return body.access_token as string;
}

export async function apiFetch<T = unknown>(
  path: string,
  init: RequestInit = {},
): Promise<{ ok: boolean; status: number; data: T }> {
  const doFetch = (token: string | null) => {
    const headers = new Headers(init.headers);
    if (token) headers.set("Authorization", `Bearer ${token}`);
    if (!headers.has("Content-Type") && init.body && typeof init.body === "string") {
      headers.set("Content-Type", "application/json");
    }
    return fetch(`${BASE}${path}`, {
      ...init,
      headers,
      credentials: "include",
    });
  };

  const { accessToken } = useAuthStore.getState();
  let res = await doFetch(accessToken);

  if (res.status === 401 && accessToken) {
    // Attempt a single coordinated refresh
    if (!refreshPromise) {
      refreshPromise = refreshAccessToken().finally(() => {
        refreshPromise = null;
      });
    }

    const newToken = await refreshPromise;
    if (newToken) {
      useAuthStore.getState().setAccessToken(newToken);
      res = await doFetch(newToken);
    } else {
      // Refresh failed — clear auth everywhere
      useAuthStore.getState().clearAuth();
      broadcastLogout();
    }
  }

  let data: T;
  const contentType = res.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    data = await res.json();
  } else {
    data = (await res.text()) as unknown as T;
  }
  return { ok: res.ok, status: res.status, data };
}
