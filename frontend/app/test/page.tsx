"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { useAuthStore } from "@/lib/auth/store";
import { initAuthSync, broadcastLogout } from "@/lib/auth/sync";
import * as api from "@/lib/client/api";

/* ------------------------------------------------------------------ */
/*  Types                                                              */
/* ------------------------------------------------------------------ */

interface LogEntry {
  id: number;
  ts: string;
  method: string;
  path: string;
  status: number;
  ok: boolean;
  body: string;
}

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */

export default function TestPage() {
  // auth state
  const { accessToken, user, setAuth, clearAuth, setAccessToken } =
    useAuthStore();

  // response log
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const logIdRef = useRef(0);

  // form fields
  const [regEmail, setRegEmail] = useState("");
  const [regPassword, setRegPassword] = useState("");
  const [regName, setRegName] = useState("");
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [userUuid, setUserUuid] = useState("");
  const [oldPw, setOldPw] = useState("");
  const [newPw, setNewPw] = useState("");

  useEffect(() => {
    initAuthSync();
  }, []);

  /* helper to log every API call */
  const log = useCallback(
    (method: string, path: string, res: { ok: boolean; status: number; data: unknown }) => {
      setLogs((prev) => [
        {
          id: ++logIdRef.current,
          ts: new Date().toLocaleTimeString(),
          method,
          path,
          status: res.status,
          ok: res.ok,
          body: JSON.stringify(res.data, null, 2),
        },
        ...prev.slice(0, 49), // keep last 50
      ]);
    },
    [],
  );

  /* ---- actions ---- */

  const handleRegister = async () => {
    const res = await api.register({
      email: regEmail,
      password: regPassword,
      name: regName,
    });
    log("POST", "/auth/register", res);
    if (res.ok) {
      const d = res.data;
      setAuth(d.access_token, d.user);
    }
  };

  const handleLogin = async () => {
    const res = await api.login(loginEmail, loginPassword);
    log("POST", "/auth/login", res);
    if (res.ok) {
      const d = res.data;
      setAuth(d.access_token, d.user);
    }
  };

  const handleGoogleLogin = () => {
    api.googleLoginRedirect();
  };

  const handleRefresh = async () => {
    const res = await api.refresh();
    log("POST", "/auth/refresh", res);
    if (res.ok) {
      setAccessToken((res.data as { access_token: string }).access_token);
    }
  };

  const handleLogout = async () => {
    const res = await api.logout();
    log("POST", "/auth/logout", res);
    clearAuth();
    broadcastLogout();
  };

  const handleMe = async () => {
    const res = await api.me();
    log("GET", "/auth/me", res);
  };

  const handleGetUser = async () => {
    const res = await api.getUser(userUuid);
    log("GET", `/users/${userUuid}`, res);
  };

  const handleGetAll = async () => {
    const res = await api.listUsers();
    log("GET", "/users", res);
  };

  const handleDeleteUser = async () => {
    const res = await api.deleteUser(userUuid);
    log("DELETE", `/users/${userUuid}`, res);
  };

  const handleUpdatePw = async () => {
    if (!user) return;
    const res = await api.updatePassword(user.uuid, oldPw, newPw);
    log("PUT", `/users/${user.uuid}/password`, res);
  };

  const handleCountUsers = async () => {
    const res = await api.countUsers();
    log("GET", "/users/count", res);
  };



  /* ================================================================ */
  /*  Render                                                           */
  /* ================================================================ */

  const inputCls =
    "w-full rounded border border-gray-600 bg-gray-800 px-3 py-2 text-sm text-white placeholder:text-gray-500 focus:border-blue-500 focus:outline-none";
  const btnCls =
    "rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-40";
  const btnAltCls =
    "rounded bg-gray-700 px-4 py-2 text-sm font-medium text-white hover:bg-gray-600";
  const btnDangerCls =
    "rounded bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-500";

  return (
    <div className="min-h-screen bg-gray-950 p-6 text-white">
      <h1 className="mb-6 text-2xl font-bold">API Test Dashboard</h1>

      {/* ---- token info bar ---- */}
      <section className="mb-6 rounded-lg border border-gray-800 bg-gray-900 p-4">
        <h2 className="mb-2 text-lg font-semibold">Session</h2>
        <p className="text-sm text-gray-400">
          <span className="font-medium text-gray-300">Token:</span>{" "}
          {accessToken ? `${accessToken.slice(0, 24)}…` : "none"}
        </p>
        <p className="text-sm text-gray-400">
          <span className="font-medium text-gray-300">User:</span>{" "}
          {user ? `${user.name} (${user.registered_email}) — ${user.access_level}` : "not logged in"}
        </p>
      </section>

      <div className="grid gap-6 lg:grid-cols-2 xl:grid-cols-3">
        {/* ---- Register ---- */}
        <Panel title="Register">
          <input className={inputCls} placeholder="Email" value={regEmail} onChange={(e) => setRegEmail(e.target.value)} />
          <input className={inputCls} placeholder="Password" type="password" value={regPassword} onChange={(e) => setRegPassword(e.target.value)} />
          <input className={inputCls} placeholder="Name" value={regName} onChange={(e) => setRegName(e.target.value)} />
          <button className={btnCls} onClick={handleRegister}>Register</button>
        </Panel>

        {/* ---- Login ---- */}
        <Panel title="Login">
          <input className={inputCls} placeholder="Email" value={loginEmail} onChange={(e) => setLoginEmail(e.target.value)} />
          <input className={inputCls} placeholder="Password" type="password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} />
          <button className={btnCls} onClick={handleLogin}>Login (email)</button>
          <button className={btnAltCls} onClick={handleGoogleLogin}>Login with Google</button>
        </Panel>

        {/* ---- Session actions ---- */}
        <Panel title="Session">
          <button className={btnCls} onClick={handleRefresh}>Refresh token</button>
          <button className={btnCls} onClick={handleMe}>Who am I? (/me)</button>
          <button className={btnDangerCls} onClick={handleLogout}>Logout</button>
        </Panel>

        {/* ---- Users ---- */}
        <Panel title="Users">
          <input className={inputCls} placeholder="UUID" value={userUuid} onChange={(e) => setUserUuid(e.target.value)} />
          <div className="flex flex-wrap gap-2">
            <button className={btnAltCls} onClick={handleGetUser}>Get user</button>
            <button className={btnAltCls} onClick={handleGetAll}>All users</button>
            <button className={btnAltCls} onClick={handleCountUsers}>Count</button>
            <button className={btnDangerCls} onClick={handleDeleteUser}>Delete</button>
          </div>
        </Panel>

        {/* ---- Update password ---- */}
        <Panel title="Update Password">
          <input className={inputCls} placeholder="Current password" type="password" value={oldPw} onChange={(e) => setOldPw(e.target.value)} />
          <input className={inputCls} placeholder="New password" type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} />
          <button className={btnCls} onClick={handleUpdatePw} disabled={!user}>Update</button>
        </Panel>
      </div>

      {/* ---- Response log ---- */}
      <section className="mt-8">
        <div className="mb-2 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Response Log</h2>
          <button className="text-xs text-gray-500 hover:text-gray-300" onClick={() => setLogs([])}>
            Clear
          </button>
        </div>
        <div className="max-h-[450px] space-y-2 overflow-y-auto rounded-lg border border-gray-800 bg-gray-900 p-3">
          {logs.length === 0 && <p className="text-sm text-gray-600">No requests yet.</p>}
          {logs.map((entry) => (
            <details key={entry.id} className="group rounded border border-gray-800 bg-gray-950">
              <summary className="flex cursor-pointer items-center gap-3 px-3 py-2 text-sm">
                <span className={entry.ok ? "text-green-400" : "text-red-400"}>{entry.status}</span>
                <span className="font-mono text-gray-400">{entry.method}</span>
                <span className="text-gray-300">{entry.path}</span>
                <span className="ml-auto text-xs text-gray-600">{entry.ts}</span>
              </summary>
              <pre className="max-h-64 overflow-auto whitespace-pre-wrap px-3 pb-3 text-xs text-gray-400">
                {entry.body}
              </pre>
            </details>
          ))}
        </div>
      </section>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Panel helper                                                       */
/* ------------------------------------------------------------------ */

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="flex flex-col gap-3 rounded-lg border border-gray-800 bg-gray-900 p-4">
      <h2 className="text-base font-semibold">{title}</h2>
      {children}
    </section>
  );
}
