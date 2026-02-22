"use client";

import React from "react";
import {
  Mail,
  Users,
  FileSpreadsheet,
  BarChart3,
  ShieldAlert,
  Bot,
  BrainCircuit,
} from "lucide-react";

interface BentoCardProps {
  title: string;
  description: React.ReactNode;
  icon: React.ReactNode;
  className?: string;
  bgContent?: React.ReactNode;
}

const BentoCard: React.FC<BentoCardProps> = ({
  title,
  description,
  icon,
  className = "",
  bgContent,
}) => (
  <div
    className={`relative overflow-hidden rounded-3xl bg-gray-50 border border-gray-200 p-8 hover:shadow-lg transition-shadow duration-300 group ${className}`}
  >
    <div className="relative z-10 flex flex-col h-full justify-between pointer-events-none">
      <div className="mb-8">
        <div className="w-10 h-10 rounded-full bg-white border border-gray-200 flex items-center justify-center mb-4 text-gray-900 shadow-sm group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
        <div className="text-gray-500 text-sm leading-relaxed">
          {description}
        </div>
      </div>
    </div>
    {bgContent}
  </div>
);

const agentSteps = [
  { text: "Loading company CSV — 500 entries...", color: "text-blue-400" },
  { text: "Mapped: Name, Email, Role fields", color: "text-green-400" },
  { text: "Personalizing templates per company...", color: "text-purple-400" },
  { text: "Awaiting admin approval before send...", color: "text-gray-400" },
];

const BentoGrid: React.FC = () => {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-16 max-w-3xl">
          <h2 className="text-4xl font-bold text-gray-900 mb-6 tracking-tight">
            Everything the T&P Cell needs <br />
            <span className="text-gray-500">
              to automate placement outreach.
            </span>
          </h2>
          <p className="text-lg text-gray-600">
            CorpoMailer gives DTU&apos;s Training &amp; Placement Cell the
            tools to send, manage, and track corporate emails at scale — with
            group management, shared templates, and admin oversight built in.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[300px]">
          {/* Large Card 1 - Approval Workflow */}
          <BentoCard
            title="Admin Approval Workflow"
            description={
              <span className="block md:max-w-[50%]">
                Coordinators draft campaigns and admins review them before
                anything is sent. Edit, reject, or approve every email with
                full control.
              </span>
            }
            icon={<ShieldAlert size={20} />}
            className="md:col-span-2 bg-gradient-to-br from-blue-50 to-indigo-50"
            bgContent={
              <div className="absolute right-0 bottom-0 w-[260px] md:w-[320px] h-[180px] md:h-[220px] translate-x-8 translate-y-8 group-hover:translate-x-4 group-hover:translate-y-4 transition-transform duration-500">
                <div className="bg-white rounded-tl-2xl border-t border-l border-gray-200 shadow-xl p-5 h-full flex flex-col gap-3">
                  <div className="flex items-center justify-between border-b border-gray-100 pb-2">
                    <span className="text-[10px] font-bold text-orange-500 bg-orange-100 px-2 py-0.5 rounded">
                      WAITING FOR HUMAN
                    </span>
                    <span className="text-[10px] text-gray-400">
                      Agent: Sales-Bot-01
                    </span>
                  </div>
                  <div className="space-y-2">
                    <div className="h-1.5 w-full bg-gray-100 rounded" />
                    <div className="h-1.5 w-5/6 bg-gray-100 rounded" />
                    <div className="h-1.5 w-4/6 bg-gray-100 rounded" />
                  </div>
                  <div className="flex gap-2 mt-auto">
                    <button className="bg-black text-white text-[10px] px-3 py-1.5 rounded hover:bg-gray-800 transition-colors">
                      Approve
                    </button>
                    <button className="bg-white border border-gray-200 text-[10px] px-3 py-1.5 rounded hover:bg-gray-50 transition-colors">
                      Rewrite
                    </button>
                  </div>
                </div>
              </div>
            }
          />

          {/* Card 2 - CSV */}
          <BentoCard
            title="Bulk CSV Import"
            description="Upload your company contact list — up to 500 entries. CorpoMailer auto-maps fields and personalizes every email automatically."
            icon={<FileSpreadsheet size={20} />}
            className="bg-white"
          />

          {/* Card 3 - Agents (Dark) */}
          <div className="relative overflow-hidden rounded-3xl bg-gray-900 border border-gray-800 p-8 hover:shadow-lg transition-shadow duration-300 group md:row-span-2">
            <div className="relative z-10 flex flex-col h-full justify-between pointer-events-none">
              <div className="mb-8">
                <div className="w-10 h-10 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center mb-4 text-white shadow-sm">
                  <Bot size={20} />
                </div>
                <h3 className="text-xl font-bold text-white mb-2">
                  Groups &amp; Shared Templates
                </h3>
                <p className="text-gray-400 text-sm leading-relaxed">
                  {"Create named groups like 'Core Companies' or 'Mass Recruiters', build email templates once, and share them across the entire T&P team."}
                </p>
              </div>
              <div className="flex flex-col gap-3 mt-4 font-mono text-xs">
                {agentSteps.map((step, i) => (
                  <div
                    key={i}
                    className="flex items-center gap-3 p-3 bg-gray-800/50 rounded-lg border border-gray-700/50"
                  >
                    <div
                      className={`w-1.5 h-1.5 rounded-full ${i === agentSteps.length - 1
                          ? "bg-gray-500 animate-pulse"
                          : "bg-green-500"
                        }`}
                    />
                    <div className={step.color}>{step.text}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Card 4 - AI */}
          <BentoCard
            title="Personalized per Company"
            description="Each email is tailored with the company name, contact, and role from your CSV — no generic blasts."
            icon={<BrainCircuit size={20} />}
          />

          {/* Card 5 - Smart Groups */}
          <BentoCard
            title="Smart Contact Groups"
            description="Segment companies into groups and target the right audience for each campaign — placement, internship, or custom drives."
            icon={<Users size={20} />}
          />

          {/* Card 6 - Wide */}
          <BentoCard
            title="Campaign Tracking"
            description={
              <span className="block md:max-w-[50%]">
                Track delivery and open rates per campaign in real-time. See
                which companies engaged and follow up at the right time.
              </span>
            }
            icon={<BarChart3 size={20} />}
            className="md:col-span-2"
            bgContent={
              <div className="absolute right-0 top-1/2 -translate-y-1/2 w-[40%] h-full opacity-50 p-6 flex items-center justify-center pointer-events-none">
                <div className="w-full h-32 flex items-end gap-2">
                  {[40, 60, 30, 80, 50, 90].map((h, i) => (
                    <div
                      key={i}
                      className="w-full rounded-t"
                      style={{
                        height: `${h}%`,
                        backgroundColor: `hsl(${217 + i * 5}, ${60 + i * 5}%, ${55 - i * 3}%)`,
                      }}
                    />
                  ))}
                </div>
              </div>
            }
          />
        </div>
      </div>
    </section>
  );
};

export default BentoGrid;
