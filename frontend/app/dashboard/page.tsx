"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import {
  Bot,
  Send,
  Sparkles,
  FileText,
  Loader2,
  Mail,
  Type,
  Info,
  CheckCircle,
} from "lucide-react";
import { generateEmail, type EmailTone } from "@/lib/gemini";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

const TONES: EmailTone[] = ["Casual", "Formal", "Creative"];

const UserDashboard: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  // Form state
  const [senderName, setSenderName] = useState("");
  const [senderEmail, setSenderEmail] = useState("");
  const [receiverName, setReceiverName] = useState("");
  const [receiverEmail, setReceiverEmail] = useState("");
  const [context, setContext] = useState("");
  const [tone, setTone] = useState<EmailTone>("Formal");
  const [companyName, setCompanyName] = useState("");
  const [subject, setSubject] = useState("");

  // Generation state
  const [generatedBody, setGeneratedBody] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSending, setIsSending] = useState(false);

  // Status
  const [statusMessage, setStatusMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);

  // Guard: redirect if not authenticated
  React.useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  const handleGenerate = async () => {
    if (!context || !senderName || !receiverName) {
      alert(
        "Please fill in the required fields (Sender Name, Receiver Name, Context)"
      );
      return;
    }

    setIsGenerating(true);
    setGeneratedBody("");
    setStatusMessage(null);

    try {
      const emailContent = await generateEmail(
        receiverName,
        senderName,
        companyName,
        context,
        tone
      );
      setGeneratedBody(emailContent);

      if (!subject) {
        setSubject(
          `Message from ${senderName} at ${companyName || "our company"}`
        );
      }
    } catch (error) {
      console.error("Generation failed:", error);
      setStatusMessage({ type: "error", text: "Failed to generate email." });
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSend = () => {
    if (!generatedBody) return;
    if (!subject) {
      alert("Please provide a subject line.");
      return;
    }

    setIsSending(true);
    setStatusMessage(null);

    setTimeout(() => {
      setIsSending(false);
      setStatusMessage({
        type: "success",
        text: "Email successfully sent (Simulation Mode)!",
      });
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Agent Dashboard
            </h1>
            <p className="text-gray-500">
              Deploy your AI workforce to draft and send emails.
            </p>
          </div>
        </div>

        {statusMessage && (
          <div
            className={`mb-6 border px-4 py-3 rounded-lg relative flex items-center gap-2 shadow-sm ${
              statusMessage.type === "success"
                ? "bg-green-50 border-green-200 text-green-700"
                : "bg-red-50 border-red-200 text-red-700"
            }`}
          >
            <CheckCircle size={20} />
            {statusMessage.text}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Input */}
          <div className="space-y-6">
            {/* Sender Section */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-2 border-b border-gray-100 pb-4 mb-4">
                <Bot className="text-indigo-600" size={20} />
                <h2 className="text-lg font-semibold">Sender Details</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Sender Name
                  </label>
                  <input
                    type="text"
                    value={senderName}
                    onChange={(e) => setSenderName(e.target.value)}
                    placeholder="John Doe"
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Company Name
                  </label>
                  <input
                    type="text"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    placeholder="Acme Corp"
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all text-sm"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Sender Email
                </label>
                <div className="relative">
                  <Mail
                    className="absolute left-3 top-2.5 text-gray-400"
                    size={16}
                  />
                  <input
                    type="email"
                    value={senderEmail}
                    onChange={(e) => setSenderEmail(e.target.value)}
                    placeholder="you@company.com"
                    className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Recipient & Context */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 space-y-4">
              <div className="flex items-center gap-2 border-b border-gray-100 pb-4 mb-4">
                <Info className="text-indigo-600" size={20} />
                <h2 className="text-lg font-semibold">Message Context</h2>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Receiver Name
                  </label>
                  <input
                    type="text"
                    value={receiverName}
                    onChange={(e) => setReceiverName(e.target.value)}
                    placeholder="Jane Smith"
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Receiver Email
                  </label>
                  <input
                    type="email"
                    value={receiverEmail}
                    onChange={(e) => setReceiverEmail(e.target.value)}
                    placeholder="jane@target.com"
                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all text-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Subject Line
                </label>
                <div className="relative">
                  <Type
                    className="absolute left-3 top-2.5 text-gray-400"
                    size={16}
                  />
                  <input
                    type="text"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    placeholder="Subject will be auto-generated if left blank"
                    className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all text-sm"
                  />
                </div>
              </div>

              {/* Tone Selector */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  AI Persona & Tone
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {TONES.map((t) => (
                    <button
                      key={t}
                      type="button"
                      onClick={() => setTone(t)}
                      className={`py-2 px-3 rounded-lg text-xs font-medium border transition-all ${
                        tone === t
                          ? "bg-black text-white border-black"
                          : "bg-white text-gray-600 border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>

              {/* Context */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Context / Instructions
                </label>
                <textarea
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  placeholder="What is this email about? E.g. 'Ask for a meeting next Tuesday to discuss the Q3 marketing report'..."
                  className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-black focus:border-transparent outline-none transition-all h-28 resize-none text-sm"
                />
              </div>

              <button
                type="button"
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full bg-black text-white py-3 rounded-xl font-bold text-lg hover:bg-gray-800 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg hover:-translate-y-0.5"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="animate-spin" /> Generating...
                  </>
                ) : (
                  <>
                    <Sparkles size={18} /> Generate Draft
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Right Column: Preview */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col h-full">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-4 mb-4">
              <FileText className="text-indigo-600" size={20} />
              <h2 className="text-lg font-semibold">Live Preview</h2>
            </div>

            <div className="flex-grow bg-gray-50 rounded-xl border border-gray-200 p-4 font-mono text-sm whitespace-pre-wrap overflow-y-auto mb-4 relative group">
              {generatedBody ? (
                <textarea
                  className="w-full h-full bg-transparent outline-none resize-none text-gray-800"
                  value={generatedBody}
                  onChange={(e) => setGeneratedBody(e.target.value)}
                />
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-gray-400">
                  <Bot size={48} className="mb-4 opacity-20" />
                  <p>AI output will appear here.</p>
                </div>
              )}
            </div>

            <div className="mt-auto">
              <button
                type="button"
                onClick={handleSend}
                disabled={!generatedBody || isSending}
                className="w-full bg-indigo-600 text-white py-3 rounded-xl font-bold text-lg hover:bg-indigo-700 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-200 hover:-translate-y-0.5"
              >
                {isSending ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <Send size={18} />
                )}
                Send Email
              </button>
              <p className="text-xs text-center text-gray-400 mt-3">
                Runs in Simulation Mode. No emails are actually sent.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
