"use client";

import React, { useState } from "react";
import {
  Terminal,
  Cpu,
  ArrowRight,
  Key,
  Shield,
  Zap,
  Code2,
  Globe,
} from "lucide-react";

const campaignCode = `import { CorpoMailer } from "@corpomailer/sdk";

const mailer = new CorpoMailer({ apiKey: "cm_sk_..." });

// Create a high-volume campaign with approval flow
const campaign = await mailer.campaigns.create({
  name: "Q3 Investor Outreach",
  template: "investor-intro-v2",
  audience: {
    csv: "./investors.csv", // Contains Name, Email, Firm
    filter: "industry = 'SaaS'"
  },
  schedule: "2024-10-15T10:00:00Z",
  approvalRequired: true
});

console.log(\`Campaign created: \${campaign.id}\`);
// Output: Campaign created: cam_123456 (Status: Pending Approval)`;

const transactionalCode = `import { CorpoMailer } from "@corpomailer/sdk";

const mailer = new CorpoMailer({ apiKey: process.env.CM_KEY });

// Send a single real-time transactional email
await mailer.send({
  to: "alex.rivera@example.com",
  template: "welcome-dashboard",
  data: {
    firstName: "Alex",
    company: "TechFlow",
    loginLink: "https://app.corpomailer.com/login?token=..."
  },
  trackOpens: true
});

console.log("Welcome email sent!");`;

const CodeBlock: React.FC<{ code: string }> = ({ code }) => (
  <div className="bg-[#0d1117] p-6 rounded-b-xl overflow-x-auto text-sm font-mono leading-relaxed text-gray-300">
    <pre style={{ margin: 0 }}>{code}</pre>
  </div>
);

const devFeatures = [
  {
    icon: <Cpu className="text-indigo-600" size={24} />,
    title: "REST & GraphQL API",
    desc: "Fully typed SDKs for Node, Python, and Go. Or use our comprehensive GraphQL API for flexible data fetching.",
  },
  {
    icon: <Key className="text-indigo-600" size={24} />,
    title: "Scoped API Keys",
    desc: "Generate limited-access keys for different environments. Perfect for CI/CD pipelines and staging servers.",
  },
  {
    icon: <Shield className="text-indigo-600" size={24} />,
    title: "Compliance Built-in",
    desc: "Automatic handling of unsubscribe links, bounce processing, and GDPR data subject requests.",
  },
  {
    icon: <Globe className="text-indigo-600" size={24} />,
    title: "Global CDN",
    desc: "Email assets are served from edge locations worldwide, ensuring fast load times for your recipients.",
  },
  {
    icon: <Code2 className="text-indigo-600" size={24} />,
    title: "Webhooks",
    desc: "Receive real-time events for opens, clicks, and bounces. Sync email engagement data back to your CRM.",
  },
  {
    icon: <Zap className="text-indigo-600" size={24} />,
    title: "99.99% Uptime",
    desc: "Enterprise-grade reliability with redundant infrastructure providers across multiple availability zones.",
  },
];

const stats = [
  { label: "Emails / Day", value: "500M+" },
  { label: "Deliverability", value: "99.8%" },
  { label: "API Latency", value: "<100ms" },
  { label: "Active Devs", value: "10k+" },
];

const DeveloperPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"campaign" | "transactional">(
    "campaign"
  );

  return (
    <div className="bg-white min-h-screen text-gray-900 pt-24 font-sans">
      {/* Dev Hero */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="absolute inset-0 -z-10 h-full w-full bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]" />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div className="relative z-10">
            <div className="inline-flex items-center gap-2 text-indigo-600 font-mono text-xs font-semibold mb-8 border border-indigo-100 bg-indigo-50 px-3 py-1.5 rounded-full uppercase tracking-wider">
              <Terminal size={12} />
              <span>Developers First</span>
            </div>
            <h1 className="text-5xl sm:text-6xl font-bold tracking-tight mb-6 leading-[1.1] text-gray-900">
              The Headless <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-gray-700 to-gray-500">
                Email Infrastructure.
              </span>
            </h1>
            <p className="text-xl text-gray-600 mb-10 leading-relaxed max-w-lg">
              Programmatically manage campaigns, templates, and contact lists.
              Build custom outreach interfaces while leveraging our delivery and
              compliance engine.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-black text-white px-8 py-4 rounded-xl font-bold hover:bg-gray-800 transition-all hover:-translate-y-1 shadow-lg hover:shadow-xl flex items-center justify-center gap-2">
                Read Documentation <ArrowRight size={18} />
              </button>
              <button className="bg-white text-gray-900 px-8 py-4 rounded-xl font-bold border-2 border-gray-200 hover:border-gray-900 transition-colors flex items-center justify-center">
                Get API Keys
              </button>
            </div>

            <div className="mt-12 flex items-center gap-4 text-sm text-gray-500">
              <div className="flex -space-x-2">
                {["A", "B", "C", "D"].map((letter) => (
                  <div
                    key={letter}
                    className="w-8 h-8 rounded-full bg-gray-200 border-2 border-white flex items-center justify-center text-xs font-bold text-gray-600"
                  >
                    {letter}
                  </div>
                ))}
              </div>
              <p>Trusted by 4,000+ developers</p>
            </div>
          </div>

          <div className="relative lg:mt-0 mt-10 group">
            <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-2xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity duration-500" />

            <div className="relative bg-[#0d1117] rounded-xl shadow-2xl overflow-hidden border border-gray-800 ring-1 ring-white/10">
              {/* Window Chrome */}
              <div className="flex items-center justify-between px-4 py-3 bg-[#161b22] border-b border-gray-800">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
                  <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
                  <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
                </div>
                <div className="flex bg-black/20 rounded-lg p-1 text-xs font-medium">
                  <button
                    onClick={() => setActiveTab("campaign")}
                    className={`px-3 py-1 rounded-md transition-all ${
                      activeTab === "campaign"
                        ? "bg-gray-700 text-white shadow-sm"
                        : "text-gray-400 hover:text-gray-300"
                    }`}
                  >
                    Campaigns
                  </button>
                  <button
                    onClick={() => setActiveTab("transactional")}
                    className={`px-3 py-1 rounded-md transition-all ${
                      activeTab === "transactional"
                        ? "bg-gray-700 text-white shadow-sm"
                        : "text-gray-400 hover:text-gray-300"
                    }`}
                  >
                    Transactional
                  </button>
                </div>
              </div>

              {/* Code Area */}
              <div className="relative">
                <div
                  className={`transition-opacity duration-300 ${
                    activeTab === "campaign" ? "opacity-100" : "opacity-0 absolute inset-0"
                  }`}
                >
                  <CodeBlock code={campaignCode} />
                </div>
                <div
                  className={`transition-opacity duration-300 ${
                    activeTab === "transactional"
                      ? "opacity-100"
                      : "opacity-0 absolute inset-0"
                  }`}
                >
                  <CodeBlock code={transactionalCode} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Dev Features */}
      <section className="py-24 bg-gray-50 border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Everything needed to build custom email apps
            </h2>
            <p className="text-gray-600 text-lg">
              {"Don't reinvent the wheel. We handle IP reputation, deliverability, and compliance so you can focus on the product."}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {devFeatures.map((feature, i) => (
              <div
                key={i}
                className="group p-8 rounded-2xl bg-white border border-gray-200 hover:border-indigo-100 hover:shadow-xl hover:shadow-indigo-100/50 transition-all duration-300"
              >
                <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3 text-gray-900 group-hover:text-indigo-600 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-gray-500 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-black rounded-3xl p-12 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-96 h-96 bg-gray-800 rounded-full blur-3xl opacity-20 -translate-y-1/2 translate-x-1/2" />
            <div className="relative z-10 flex flex-col md:flex-row justify-between items-center gap-12">
              <div className="text-left md:w-1/3">
                <h2 className="text-3xl font-bold text-white mb-4">
                  Built for scale
                </h2>
                <p className="text-gray-400">
                  Sending millions of emails daily. Reliability you can trust
                  for your most critical outreach infrastructure.
                </p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 w-full md:w-2/3">
                {stats.map((stat) => (
                  <div
                    key={stat.label}
                    className="p-6 bg-gray-900 rounded-2xl border border-gray-800 hover:border-gray-600 transition-colors group text-center"
                  >
                    <div className="text-3xl font-bold text-white mb-2 group-hover:scale-110 transition-transform">
                      {stat.value}
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-widest font-semibold">
                      {stat.label}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default DeveloperPage;
