"use client";

import React from "react";
import {
  ShieldCheck,
  UserCheck,
  Bot,
  Sparkles,
  Sliders,
  Search,
  Globe,
  MessageSquare,
} from "lucide-react";

const FeatureDetails: React.FC = () => {
  return (
    <div className="py-24 space-y-32 bg-white">
      {/* Feature 1: Admin Workflow */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row items-center gap-16">
          <div className="flex-1">
            <div className="inline-flex items-center gap-2 text-indigo-600 font-semibold mb-6 bg-indigo-50 px-3 py-1 rounded-full text-sm">
              <ShieldCheck size={16} />
              <span>Governance & Control</span>
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Sleep soundly with Admin Approval Workflows.
            </h2>
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">
              Enable your agents and team members to draft campaigns without the
              risk of accidental sends. Admins receive a unified dashboard to
              review, edit, comment, and approve every single email before
              it&apos;s scheduled.
            </p>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <div className="mt-1 bg-green-100 p-1 rounded text-green-600">
                  <UserCheck size={16} />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">
                    Role-based Permissions
                  </h4>
                  <p className="text-gray-500 text-sm">
                    Define who can draft, who can edit, and who can approve.
                  </p>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="mt-1 bg-green-100 p-1 rounded text-green-600">
                  <Sliders size={16} />
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">
                    Content Guardrails
                  </h4>
                  <p className="text-gray-500 text-sm">
                    Automatically flag keywords or tone issues before admin
                    review.
                  </p>
                </div>
              </li>
            </ul>
          </div>

          <div className="flex-1 relative">
            <div className="bg-gray-50 rounded-2xl border border-gray-200 p-8 shadow-2xl relative z-10">
              <div className="flex justify-between items-center mb-6 border-b border-gray-100 pb-4">
                <div>
                  <h3 className="font-bold text-gray-900">Review Queue</h3>
                  <p className="text-sm text-gray-500">3 Campaigns Pending</p>
                </div>
                <button className="bg-black text-white px-4 py-2 rounded-lg text-sm font-medium">
                  Bulk Action
                </button>
              </div>
              <div className="space-y-4">
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-sm">Investor Update Q3</p>
                    <p className="text-xs text-gray-500">
                      Drafted by: AI Agent 01 • 450 Recipients
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <button className="text-xs bg-green-50 text-green-600 px-3 py-1 rounded font-medium border border-green-100">
                      Approve
                    </button>
                    <button className="text-xs bg-red-50 text-red-600 px-3 py-1 rounded font-medium border border-red-100">
                      Reject
                    </button>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between opacity-60">
                  <div>
                    <p className="font-semibold text-sm">
                      Cold Outreach: SaaS Founders
                    </p>
                    <p className="text-xs text-gray-500">
                      Drafted by: Mike T. • 120 Recipients
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <div className="h-6 w-16 bg-gray-100 rounded" />
                    <div className="h-6 w-16 bg-gray-100 rounded" />
                  </div>
                </div>
              </div>
            </div>
            <div className="absolute -top-10 -right-10 w-64 h-64 bg-indigo-100 rounded-full blur-3xl -z-10" />
          </div>
        </div>
      </div>

      {/* Feature 2: Agentic Workflow */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col lg:flex-row-reverse items-center gap-16">
          <div className="flex-1">
            <div className="inline-flex items-center gap-2 text-blue-600 font-semibold mb-6 bg-blue-50 px-3 py-1 rounded-full text-sm">
              <Bot size={16} />
              <span>Agentic Workflow</span>
            </div>
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Hire AI Agents, not just lists.
            </h2>
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">
              Define your ideal customer profile and let our autonomous agents
              scour the web. They verify emails, analyze company news, and
              identify trigger events to craft messages that actually get read.
            </p>
            <button className="text-blue-600 font-semibold flex items-center gap-2 hover:gap-4 transition-all">
              Configure your agent <span className="text-xl">→</span>
            </button>
          </div>

          <div className="flex-1 relative">
            <div className="bg-gray-900 rounded-2xl border border-gray-800 shadow-xl overflow-hidden font-mono text-sm relative">
              {/* Header */}
              <div className="bg-gray-800/50 px-4 py-3 border-b border-gray-700 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-gray-200 font-medium">
                    Agent-X (Research Mode)
                  </span>
                </div>
                <span className="text-xs text-gray-500">Live Feed</span>
              </div>

              {/* Activity Feed */}
              <div className="p-6 space-y-6 h-80 overflow-y-auto">
                <div className="flex gap-4">
                  <div className="mt-1 bg-blue-500/10 p-1.5 rounded text-blue-400 h-fit">
                    <Search size={14} />
                  </div>
                  <div className="space-y-1">
                    <p className="text-gray-300">
                      Searching for{" "}
                      <span className="text-blue-300">
                        &quot;Series A Fintech Founders&quot;
                      </span>{" "}
                      in New York.
                    </p>
                    <p className="text-xs text-gray-500">
                      Source: Crunchbase, LinkedIn, News API
                    </p>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="mt-1 bg-purple-500/10 p-1.5 rounded text-purple-400 h-fit">
                    <Globe size={14} />
                  </div>
                  <div className="space-y-1">
                    <p className="text-gray-300">
                      Identified Lead:{" "}
                      <span className="text-white font-bold">Sarah Chen</span>{" "}
                      (CEO at PayFlow)
                    </p>
                    <div className="bg-gray-800 p-2 rounded border border-gray-700 text-xs text-gray-400 mt-1">
                      <span className="text-green-400">✓</span> Recent News:
                      PayFlow raises $12M Series A
                    </div>
                  </div>
                </div>

                <div className="flex gap-4">
                  <div className="mt-1 bg-yellow-500/10 p-1.5 rounded text-yellow-400 h-fit">
                    <Sparkles size={14} />
                  </div>
                  <div className="space-y-2 w-full">
                    <p className="text-gray-300">
                      Drafting personalized hook...
                    </p>
                    <div className="bg-gray-800/50 p-3 rounded border-l-2 border-yellow-500 text-gray-400 italic text-xs">
                      &quot;Hi Sarah, saw the news about the $12M raise for
                      PayFlow—congrats on the Series A! Loved your point in the
                      TechCrunch interview about...&quot;
                    </div>
                  </div>
                </div>
              </div>

              <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-gray-900 to-transparent pointer-events-none" />
            </div>

            <div className="absolute -bottom-10 -left-10 w-72 h-72 bg-blue-500/20 rounded-full blur-3xl -z-10" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeatureDetails;
