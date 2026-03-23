import Link from "next/link";
import { ArrowLeft } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-white pt-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <Link href="/" className="inline-flex items-center gap-2 text-blue-600 hover:underline mb-8">
          <ArrowLeft size={16} />
          Back to Home
        </Link>

        <h1 className="text-5xl font-bold text-gray-900 mb-6">About CorpoMailer</h1>
        
        <div className="prose prose-lg max-w-none text-gray-600 space-y-6">
          <p className="text-xl leading-relaxed">
            CorpoMailer is the email automation platform built specifically for DTU&apos;s Training & Placement Cell to streamline corporate outreach.
          </p>

          <h2 className="text-3xl font-bold text-gray-900 mt-12 mb-4">T&P Workflow Automation</h2>
          <p>
            Our platform automates the entire placement outreach workflow, enabling T&P coordinators to:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li>Send personalized emails to 500+ companies in one click</li>
            <li>Manage groups and share templates across teams</li>
            <li>Maintain admin approval workflows for quality control</li>
            <li>Track engagement and responses in real-time</li>
            <li>Collaborate with AI agents for content generation</li>
          </ul>

          <h2 className="text-3xl font-bold text-gray-900 mt-12 mb-4">Built for Scale</h2>
          <p>
            CorpoMailer handles high-volume outreach while maintaining personalization and governance. Every email is reviewed, every template is shared, and every coordinator has the tools they need to succeed.
          </p>

          <h2 className="text-3xl font-bold text-gray-900 mt-12 mb-4">Our Mission</h2>
          <p>
            To empower placement cells with modern automation tools that save time, increase reach, and improve placement outcomes for students.
          </p>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-200">
          <Link href="/contact" className="text-blue-600 hover:underline font-medium">
            Get in touch →
          </Link>
        </div>
      </div>
    </div>
  );
}
