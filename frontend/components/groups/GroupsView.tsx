"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { ResourceCardsGrid, ResourceCardItem } from "@/components/ui/resource-cards-grid";

export type Group = {
  id: string;
  name: string;
  description: string;
  status: "not_member" | "pending" | "member";
};

const MOCK_GROUPS: Group[] = [
  { id: "1", name: "Engineering Team", description: "All engineers", status: "member" },
  { id: "2", name: "Sales Department", description: "Sales and outreach", status: "member" },
  { id: "3", name: "HR Group", description: "Human resources templates", status: "member" },
];

export const GroupsView: React.FC = () => {
  const [groups, setGroups] = useState<Group[]>(MOCK_GROUPS);
  const router = useRouter();

  const handleRequestJoin = (groupId: string) => {
    setGroups(groups.map((g) => (g.id === groupId ? { ...g, status: "pending" } : g)));
  };

  const handleOpenGroup = (groupId: string) => {
    router.push(`/groups/${groupId}/templates`);
  };

  return (
    <div className="p-8 space-y-8 text-gray-900">
      <h1 className="text-3xl font-bold mb-4">Available Groups</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {groups.map((group) => (
          <div
            key={group.id}
            className="border border-gray-200 p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow bg-white"
          >
            <h2 className="text-xl font-semibold mb-2">{group.name}</h2>
            <p className="text-gray-600 mb-4">{group.description}</p>
            {group.status === "member" ? (
              <button
                onClick={() => handleOpenGroup(group.id)}
                className="w-full bg-blue-600 text-white rounded-md py-2 px-4 hover:bg-blue-700 transition"
              >
                Open Group
              </button>
            ) : group.status === "pending" ? (
              <button
                disabled
                className="w-full bg-yellow-100 text-yellow-800 rounded-md py-2 px-4 cursor-not-allowed"
              >
                Pending Approval
              </button>
            ) : (
              <button
                onClick={() => handleRequestJoin(group.id)}
                className="w-full bg-slate-100 text-slate-800 rounded-md py-2 px-4 hover:bg-slate-200 transition"
              >
                Request to Join
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
