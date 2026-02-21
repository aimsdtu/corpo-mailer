/**
 * BroadcastChannel-based multi-tab auth sync.
 *
 * When one tab logs out or refreshes, other tabs are notified
 * so they can update their in-memory state accordingly.
 */
import { useAuthStore } from "./store";

const CHANNEL_NAME = "corpo-mailer-auth";

type AuthMessage =
  | { type: "logout" }
  | { type: "login"; accessToken: string };

let channel: BroadcastChannel | null = null;

export function initAuthSync() {
  if (typeof window === "undefined") return;
  if (channel) return; // already initialised

  channel = new BroadcastChannel(CHANNEL_NAME);

  channel.onmessage = (event: MessageEvent<AuthMessage>) => {
    const msg = event.data;
    switch (msg.type) {
      case "logout":
        useAuthStore.getState().clearAuth();
        break;
      case "login":
        useAuthStore.getState().setAccessToken(msg.accessToken);
        break;
    }
  };
}

export function broadcastLogout() {
  channel?.postMessage({ type: "logout" } satisfies AuthMessage);
}

export function broadcastLogin(accessToken: string) {
  channel?.postMessage({ type: "login", accessToken } satisfies AuthMessage);
}
