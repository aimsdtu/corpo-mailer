"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { GroupsView } from "@/components/groups/GroupsView";

export default function GroupsPage() {
  const { isAuthenticated, isInitialized } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If we're fully unauthenticated and the provider is initialized
    // Usually handled by layout/provider, but added for safety
    if (isInitialized && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isInitialized, router]);

  // If loading or redirecting
  if (!isInitialized || !isAuthenticated) return <div className="p-8 mt-20">Loading...</div>;

  return (
    <div className="min-h-screen bg-white pt-20">
      <div className="max-w-7xl mx-auto">
        <GroupsView />
      </div>
    </div>
  );
}
