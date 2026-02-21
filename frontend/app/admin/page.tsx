"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import { Check, X, Clock, Mail, RefreshCw } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

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

const statusColors: Record<EmailJob["status"], string> = {
  pending: "bg-yellow-100 text-yellow-800",
  sent: "bg-green-100 text-green-800",
  approved: "bg-blue-100 text-blue-800",
  rejected: "bg-red-100 text-red-800",
};

const AdminDashboard: React.FC = () => {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();
  const [jobs, setJobs] = useState<EmailJob[]>(initialJobs);

  React.useEffect(() => {
    if (!isAuthenticated || user?.role !== "admin") {
      router.push("/login");
    }
  }, [isAuthenticated, user, router]);

  const handleApprove = (id: string) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === id ? { ...j, status: "sent" } : j))
    );
    alert("Email Approved & 'Sent' (Demo)!");
  };

  const handleReject = (id: string) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === id ? { ...j, status: "rejected" } : j))
    );
  };

  const handleDelete = (id: string) => {
    setJobs((prev) => prev.filter((j) => j.id !== id));
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Approval Queue</h1>
            <p className="text-gray-500">
              Review generated emails before they are sent.
            </p>
          </div>
          <button
            type="button"
            onClick={() => alert("Refreshed!")}
            className="p-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 text-gray-600"
            aria-label="Refresh"
          >
            <RefreshCw size={20} />
          </button>
        </div>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
          {jobs.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              <Mail size={48} className="mx-auto mb-4 opacity-20" />
              <p>No emails in queue.</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {jobs.map((job) => (
                <div
                  key={job.id}
                  className="p-6 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex flex-col md:flex-row gap-6">
                    {/* Metadata */}
                    <div className="md:w-1/4 space-y-2">
                      <div>
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[job.status]}`}
                        >
                          {job.status.toUpperCase()}
                        </span>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Sender</p>
                        <p className="font-medium text-sm text-gray-900">
                          {job.senderName}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Receiver</p>
                        <p className="font-medium text-sm text-gray-900">
                          {job.receiverName}
                        </p>
                        <p className="text-xs text-gray-500">
                          {job.receiverEmail}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Tone</p>
                        <p className="font-medium text-sm text-indigo-600">
                          {job.tone}
                        </p>
                      </div>
                      <div className="text-xs text-gray-400 pt-2 flex items-center gap-1">
                        <Clock size={12} />
                        {new Date(job.timestamp).toLocaleString()}
                      </div>
                    </div>

                    {/* Content */}
                    <div className="md:w-1/2 bg-gray-50 p-4 rounded-lg border border-gray-200 font-mono text-sm text-gray-700 whitespace-pre-wrap">
                      {job.body}
                    </div>

                    {/* Actions */}
                    <div className="md:w-1/4 flex flex-col justify-center gap-3">
                      {job.status === "pending" && (
                        <>
                          <button
                            type="button"
                            onClick={() => handleApprove(job.id)}
                            className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg text-sm font-bold flex items-center justify-center gap-2 transition-colors"
                          >
                            <Check size={16} /> Approve & Send
                          </button>
                          <button
                            type="button"
                            onClick={() => handleReject(job.id)}
                            className="w-full bg-white hover:bg-red-50 text-red-600 border border-red-200 py-2 rounded-lg text-sm font-bold flex items-center justify-center gap-2 transition-colors"
                          >
                            <X size={16} /> Reject
                          </button>
                        </>
                      )}
                      {job.status !== "pending" && (
                        <button
                          type="button"
                          onClick={() => handleDelete(job.id)}
                          className="text-gray-400 hover:text-gray-600 text-sm underline"
                        >
                          Archive
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
