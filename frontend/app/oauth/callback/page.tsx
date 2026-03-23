"use client";

import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/auth/store";
import { broadcastLogin } from "@/lib/auth/sync";
import * as api from "@/lib/client/api";

/**
 * /oauth/callback
 *
 * The backend Google OAuth flow redirects here with
 * ?access_token=<jwt> after a successful login.
 *
 * This page stores the token, fetches the user profile,
 * broadcasts the login to other tabs, and navigates to "/".
 */
export default function OAuthCallbackPage() {
    const router = useRouter();
    const { setAuth, clearAuth } = useAuthStore();
    const handled = useRef(false);

    useEffect(() => {
        if (handled.current) return;
        handled.current = true;

        const params = new URLSearchParams(window.location.search);
        const token = params.get("access_token");

        if (!token) {
            // No token — nothing to do, send them home
            router.replace("/");
            return;
        }

        // Store token immediately so subsequent API calls are authenticated
        setAuth(token, null);

        api
            .me()
            .then((res) => {
                if (res.ok) {
                    setAuth(token, res.data as any);
                    broadcastLogin(token);
                } else {
                    // Token was invalid / expired
                    clearAuth();
                }
            })
            .catch(() => {
                clearAuth();
            })
            .finally(() => {
                router.replace("/");
            });
    }, [router, setAuth, clearAuth]);

    return (
        <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black">
            <p className="text-lg text-zinc-600 dark:text-zinc-400 animate-pulse">
                Signing you in…
            </p>
        </div>
    );
}
