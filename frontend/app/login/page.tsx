"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { ShieldCheck, User, Lock, ArrowRight, AlertCircle } from "lucide-react";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const router = useRouter();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (username === "user" && password === "demo123") {
      login("user", "user");
      router.push("/groups");
    } else if (username === "admin" && password === "admin123") {
      login("admin", "admin");
      router.push("/admin");
    } else {
      setError("Invalid credentials. Please use the demo accounts.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-xl border border-gray-100">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 bg-black text-white rounded-xl flex items-center justify-center">
            <ShieldCheck size={28} />
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            Welcome back
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Sign in to access your autonomous agents.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm flex items-center gap-2">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        <form className="mt-8 space-y-6" onSubmit={handleLogin}>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Username
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User size={18} className="text-gray-400" />
                </div>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-black focus:border-black transition-colors"
                  placeholder="Enter username"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock size={18} className="text-gray-400" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-black focus:border-black transition-colors"
                  placeholder="••••••••"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black transition-all hover:-translate-y-0.5"
          >
            Sign in
            <ArrowRight size={18} className="ml-2" />
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            {"Don't have an account? "}
            <Link href="/signup" className="font-medium text-black hover:underline">
              Create free account
            </Link>
          </p>
        </div>

        <div className="mt-6 border-t border-gray-100 pt-6">
          <p className="text-xs text-center text-gray-500 uppercase tracking-wider font-semibold mb-4">
            Demo Credentials
          </p>
          <div className="grid grid-cols-2 gap-4">
            <button
              type="button"
              className="bg-gray-50 p-3 rounded-lg border border-gray-200 text-center hover:bg-gray-100 transition-colors"
              onClick={() => {
                setUsername("user");
                setPassword("demo123");
              }}
            >
              <p className="text-xs font-medium text-gray-500">User Dashboard</p>
              <p className="text-sm font-bold text-gray-900 font-mono mt-1">
                user / demo123
              </p>
            </button>
            <button
              type="button"
              className="bg-gray-50 p-3 rounded-lg border border-gray-200 text-center hover:bg-gray-100 transition-colors"
              onClick={() => {
                setUsername("admin");
                setPassword("admin123");
              }}
            >
              <p className="text-xs font-medium text-gray-500">Admin Console</p>
              <p className="text-sm font-bold text-gray-900 font-mono mt-1">
                admin / admin123
              </p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
