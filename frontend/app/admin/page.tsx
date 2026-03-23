"use client";

export const dynamic = "force-dynamic";

import React, { useState, useMemo } from "react";
import { Check, X, Clock, Mail, Users, Plus } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { GroupDataTable, GroupRequest } from "@/components/ui/group-data-table";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { ListFilter, Columns } from "lucide-react";

interface EmailJob {
  id: string;
  senderName: string;
  receiverName: string;
  receiverEmail: string;
  subject: string;
  body: string;
  status: "pending" | "approved" | "rejected" | "sent";
  tone: string;
  timestamp: string;
}

const initialJobs: EmailJob[] = [
  {
    id: "1",
    senderName: "Alex Rivera",
    receiverName: "Sarah Chen",
    receiverEmail: "sarah@example.com",
    subject: "Partnership Opportunity",
    body: "Hi Sarah,\n\nI noticed your recent funding round and wanted to congratulate you...",
    status: "pending",
    tone: "Formal",
    timestamp: new Date().toISOString(),
  },
  {
    id: "2",
    senderName: "Mike Ross",
    receiverName: "Harvey Specter",
    receiverEmail: "harvey@pearson.com",
    subject: "Case Files",
    body: "Harvey,\n\nThe files are on your desk. Let me know if you need anything else.",
    status: "sent",
    tone: "Casual",
    timestamp: new Date(Date.now() - 86400000).toISOString(),
  },
];

const initialGroupRequests: GroupRequest[] = [
  {
    id: "gr-1",
    groupName: "Engineering Team",
    userName: "John Doe",
    userEmail: "john@example.com",
    requestDate: "2025-04-28",
    contributors: [
      { src: "https://i.pravatar.cc/150?u=1", alt: "User 1", fallback: "U1" },
      { src: "https://i.pravatar.cc/150?u=2", alt: "User 2", fallback: "U2" },
    ],
    status: { text: "Pending", variant: "pending" },
  },
  {
    id: "gr-2",
    groupName: "Sales Department",
    userName: "Jane Smith",
    userEmail: "jane@example.com",
    requestDate: "2025-04-27",
    contributors: [
      { src: "https://i.pravatar.cc/150?u=3", alt: "User 3", fallback: "U3" },
    ],
    status: { text: "Pending", variant: "pending" },
  },
];

const statusColors: Record<EmailJob["status"], string> = {
  pending: "bg-yellow-100 text-yellow-800",
  sent: "bg-green-100 text-green-800",
  approved: "bg-blue-100 text-blue-800",
  rejected: "bg-red-100 text-red-800",
};

const allColumns: (keyof GroupRequest)[] = ["groupName", "userName", "userEmail", "requestDate", "contributors", "status"];

const AdminDashboard: React.FC = () => {
  const { isAuthenticated, user, isInitialized } = useAuth();
  const router = useRouter();
  const [jobs, setJobs] = useState<EmailJob[]>(initialJobs);
  const [groupRequests, setGroupRequests] = useState<GroupRequest[]>(initialGroupRequests);
  const [activeTab, setActiveTab] = useState<"emails" | "groups">("emails");
  
  // Group filters
  const [groupFilter, setGroupFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [visibleColumns, setVisibleColumns] = useState<Set<keyof GroupRequest>>(new Set(allColumns));

  const filteredGroupRequests = useMemo(() => {
    return groupRequests.filter((request) => {
      const groupMatch = groupFilter === "" || request.groupName.toLowerCase().includes(groupFilter.toLowerCase());
      const statusMatch = statusFilter === "all" || request.status.variant === statusFilter;
      return groupMatch && statusMatch;
    });
  }, [groupRequests, groupFilter, statusFilter]);

  React.useEffect(() => {
    if (isInitialized && (!isAuthenticated || user?.role !== "admin")) {
      router.push("/login");
    }
  }, [isAuthenticated, user, isInitialized, router]);

  if (!isInitialized || !isAuthenticated || user?.role !== "admin") {
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">Loading...</div>;
  }

  const handleApprove = (id: string) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === id ? { ...j, status: "sent" } : j))
    );
  };

  const handleReject = (id: string) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === id ? { ...j, status: "rejected" } : j))
    );
  };

  const handleGroupApprove = (id: string) => {
    setGroupRequests((prev) =>
      prev.map((r) => (r.id === id ? { ...r, status: { text: "Approved", variant: "approved" } } : r))
    );
  };

  const handleGroupReject = (id: string) => {
    setGroupRequests((prev) =>
      prev.map((r) => (r.id === id ? { ...r, status: { text: "Rejected", variant: "rejected" } } : r))
    );
  };

  const toggleColumn = (column: keyof GroupRequest) => {
    setVisibleColumns((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(column)) {
        newSet.delete(column);
      } else {
        newSet.add(column);
      }
      return newSet;
    });
  };

  const pendingCount = jobs.filter((j) => j.status === "pending").length;
  const pendingGroupCount = groupRequests.filter((r) => r.status.variant === "pending").length;

  return (
    <div className="min-h-screen bg-gray-50 pt-20">
      <div className="max-w-7xl mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Manage email approvals and group requests</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-gray-200">
          <button
            onClick={() => setActiveTab("emails")}
            className={`pb-4 px-4 font-medium transition-colors relative ${
              activeTab === "emails"
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            <div className="flex items-center gap-2">
              <Mail size={20} />
              Email Approvals
              {pendingCount > 0 && (
                <span className="bg-yellow-500 text-white text-xs rounded-full px-2 py-0.5">
                  {pendingCount}
                </span>
              )}
            </div>
          </button>
          <button
            onClick={() => setActiveTab("groups")}
            className={`pb-4 px-4 font-medium transition-colors relative ${
              activeTab === "groups"
                ? "text-blue-600 border-b-2 border-blue-600"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            <div className="flex items-center gap-2">
              <Users size={20} />
              Group Requests
              {pendingGroupCount > 0 && (
                <span className="bg-yellow-500 text-white text-xs rounded-full px-2 py-0.5">
                  {pendingGroupCount}
                </span>
              )}
            </div>
          </button>
        </div>

        {/* Email Approvals Tab */}
        {activeTab === "emails" && (
          <div className="space-y-6">
            {jobs.map((job) => (
              <div
                key={job.id}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-semibold text-gray-900">{job.subject}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[job.status]}`}>
                        {job.status}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <span>From: <strong>{job.senderName}</strong></span>
                      <span>To: <strong>{job.receiverName}</strong> ({job.receiverEmail})</span>
                      <span>Tone: {job.tone}</span>
                    </div>
                  </div>
                  <Clock className="text-gray-400" size={20} />
                </div>

                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <p className="text-gray-700 whitespace-pre-wrap text-sm">{job.body}</p>
                </div>

                {job.status === "pending" && (
                  <div className="flex gap-3">
                    <button
                      onClick={() => handleApprove(job.id)}
                      className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
                    >
                      <Check size={18} />
                      Approve & Send
                    </button>
                    <button
                      onClick={() => handleReject(job.id)}
                      className="flex-1 bg-red-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-red-700 transition-colors flex items-center justify-center gap-2"
                    >
                      <X size={18} />
                      Reject
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Group Requests Tab */}
        {activeTab === "groups" && (
          <div>
            <div className="flex flex-col gap-4 mb-6 sm:flex-row sm:items-center">
              <div className="flex flex-1 gap-4">
                <Input
                  placeholder="Filter by group name..."
                  value={groupFilter}
                  onChange={(e) => setGroupFilter(e.target.value)}
                  className="max-w-xs"
                />
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" className="flex items-center gap-2">
                      <ListFilter className="h-4 w-4" />
                      <span>Status</span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuLabel>Filter by Status</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuCheckboxItem checked={statusFilter === "all"} onCheckedChange={() => setStatusFilter("all")}>All</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem checked={statusFilter === "pending"} onCheckedChange={() => setStatusFilter("pending")}>Pending</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem checked={statusFilter === "approved"} onCheckedChange={() => setStatusFilter("approved")}>Approved</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem checked={statusFilter === "rejected"} onCheckedChange={() => setStatusFilter("rejected")}>Rejected</DropdownMenuCheckboxItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" className="flex items-center gap-2">
                    <Columns className="h-4 w-4" />
                    <span>Columns</span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuLabel>Toggle Columns</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  {allColumns.map((column) => (
                    <DropdownMenuCheckboxItem
                      key={column}
                      className="capitalize"
                      checked={visibleColumns.has(column)}
                      onCheckedChange={() => toggleColumn(column)}
                    >
                      {column}
                    </DropdownMenuCheckboxItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            <GroupDataTable
              requests={filteredGroupRequests}
              visibleColumns={visibleColumns}
              onApprove={handleGroupApprove}
              onReject={handleGroupReject}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
