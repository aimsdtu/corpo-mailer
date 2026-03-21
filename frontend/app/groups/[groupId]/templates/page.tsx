"use client";

import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { ResourceCardsGrid, ResourceCardItem } from "@/components/ui/resource-cards-grid";
import { X } from "lucide-react";

const MOCK_TEMPLATES: Record<string, ResourceCardItem[]> = {
  "1": [
    {
      iconSrc: "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=100&h=100&fit=crop",
      title: "Sprint Planning",
      lastUpdated: "29 April 2025",
      href: "#sprint-planning",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=100&h=100&fit=crop",
      title: "Code Review Request",
      lastUpdated: "28 April 2025",
      href: "#code-review",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=100&h=100&fit=crop",
      title: "Bug Report",
      lastUpdated: "27 April 2025",
      href: "#bug-report",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=100&h=100&fit=crop",
      title: "Feature Proposal",
      lastUpdated: "26 April 2025",
      href: "#feature-proposal",
    },
  ],
  "2": [
    {
      iconSrc: "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
      title: "Sales Outreach",
      lastUpdated: "29 April 2025",
      href: "#sales-outreach",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=100&h=100&fit=crop",
      title: "Follow-up Email",
      lastUpdated: "28 April 2025",
      href: "#follow-up",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=100&h=100&fit=crop",
      title: "Product Demo",
      lastUpdated: "27 April 2025",
      href: "#product-demo",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=100&h=100&fit=crop",
      title: "Proposal Template",
      lastUpdated: "26 April 2025",
      href: "#proposal",
    },
  ],
  "3": [
    {
      iconSrc: "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=100&h=100&fit=crop",
      title: "Offer Letter",
      lastUpdated: "29 April 2025",
      href: "#offer-letter",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=100&h=100&fit=crop",
      title: "Interview Invitation",
      lastUpdated: "28 April 2025",
      href: "#interview",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=100&h=100&fit=crop",
      title: "Onboarding Welcome",
      lastUpdated: "27 April 2025",
      href: "#onboarding",
    },
    {
      iconSrc: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=100&h=100&fit=crop",
      title: "Performance Review",
      lastUpdated: "26 April 2025",
      href: "#performance",
    },
  ],
};

const TEMPLATE_CONTENT: Record<string, { subject: string; body: string }> = {
  "sprint-planning": {
    subject: "Sprint Planning Meeting - Week of [Date]",
    body: `Hi Team,

This is a reminder for our upcoming sprint planning meeting scheduled for [Date] at [Time].

Agenda:
• Review previous sprint outcomes
• Discuss upcoming sprint goals
• Assign tasks and story points
• Address any blockers

Please come prepared with your updates and any items you'd like to discuss.

Best regards,
[Your Name]`,
  },
  "code-review": {
    subject: "Code Review Request - [PR Title]",
    body: `Hi [Reviewer Name],

I've submitted a pull request that requires your review:

PR: [PR Link]
Branch: [Branch Name]
Changes: [Brief description of changes]

Key areas to focus on:
• [Area 1]
• [Area 2]

Please let me know if you have any questions or concerns.

Thanks,
[Your Name]`,
  },
  "bug-report": {
    subject: "Critical Bug Report - [Issue Description]",
    body: `Hi Team,

I've identified a critical bug that needs immediate attention:

Issue: [Brief description]
Severity: [High/Critical]
Affected Users: [Number/Percentage]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected vs Actual Behavior:
[Description]

Please prioritize this for the current sprint.

Best regards,
[Your Name]`,
  },
  "feature-proposal": {
    subject: "Feature Proposal - [Feature Name]",
    body: `Hi Team,

I'd like to propose a new feature for consideration:

Feature: [Feature Name]
Problem it solves: [Description]
Target users: [User segment]

Benefits:
• [Benefit 1]
• [Benefit 2]
• [Benefit 3]

I'd love to discuss this further in our next planning meeting.

Thanks,
[Your Name]`,
  },
  "sales-outreach": {
    subject: "Partnership Opportunity with [Your Company]",
    body: `Hi [Prospect Name],

I hope this email finds you well. I'm reaching out from [Your Company] because I believe we can help [Their Company] achieve [specific goal].

We specialize in [your solution] and have helped companies like [Client 1] and [Client 2] achieve [specific results].

Would you be open to a brief 15-minute call next week to explore how we might work together?

Best regards,
[Your Name]
[Your Title]
[Your Company]`,
  },
  "follow-up": {
    subject: "Following Up - [Previous Topic]",
    body: `Hi [Name],

I wanted to follow up on our conversation from [Date] regarding [Topic].

Have you had a chance to [action item discussed]? I'd be happy to provide any additional information or answer questions you might have.

Looking forward to hearing from you.

Best regards,
[Your Name]`,
  },
  "product-demo": {
    subject: "Schedule Your [Product] Demo",
    body: `Hi [Prospect Name],

Thank you for your interest in [Product Name]!

I'd love to show you how [Product] can help [Their Company] [achieve specific goal]. Our demo typically takes 30 minutes and covers:

• [Feature 1]
• [Feature 2]
• [Feature 3]
• Q&A session

Are you available for a demo next week? Here are some time slots:
• [Option 1]
• [Option 2]
• [Option 3]

Looking forward to connecting!

Best regards,
[Your Name]`,
  },
  "proposal": {
    subject: "Business Proposal - [Project Name]",
    body: `Dear [Client Name],

Thank you for the opportunity to submit this proposal for [Project Name].

Overview:
[Brief project description]

Scope of Work:
• [Deliverable 1]
• [Deliverable 2]
• [Deliverable 3]

Timeline: [Duration]
Investment: [Amount]

I'm confident we can deliver exceptional results. Please let me know if you'd like to discuss any aspects of this proposal.

Best regards,
[Your Name]`,
  },
  "offer-letter": {
    subject: "Job Offer - [Position] at [Company]",
    body: `Dear [Candidate Name],

Congratulations! We are pleased to extend an offer for the position of [Job Title] at [Company Name].

Position: [Job Title]
Department: [Department]
Start Date: [Date]
Compensation: [Salary]

We believe you'll be a great addition to our team and look forward to working with you.

Please review the attached offer letter and let us know your decision by [Date].

Best regards,
[Your Name]
[Your Title]`,
  },
  "interview": {
    subject: "Interview Invitation - [Position] at [Company]",
    body: `Dear [Candidate Name],

Thank you for your application for the [Position] role at [Company Name].

We're impressed with your background and would like to invite you for an interview.

Interview Details:
Date: [Date]
Time: [Time]
Duration: [Duration]
Format: [In-person/Virtual]
Interviewers: [Names]

Please confirm your availability at your earliest convenience.

Best regards,
[Your Name]
[Your Title]`,
  },
  "onboarding": {
    subject: "Welcome to [Company]!",
    body: `Dear [New Hire Name],

Welcome to [Company Name]! We're thrilled to have you join our team.

Your first day is [Date] at [Time]. Here's what to expect:

Day 1 Agenda:
• Team introductions
• Office tour
• IT setup
• HR orientation
• Lunch with your team

What to bring:
• [Item 1]
• [Item 2]

If you have any questions before your start date, please don't hesitate to reach out.

Looking forward to working with you!

Best regards,
[Your Name]`,
  },
  "performance": {
    subject: "Performance Review Meeting - [Period]",
    body: `Hi [Employee Name],

It's time for your [Annual/Quarterly] performance review for the period [Date Range].

Meeting Details:
Date: [Date]
Time: [Time]
Duration: [Duration]

We'll discuss:
• Accomplishments and achievements
• Areas for growth
• Goals for next period
• Career development

Please come prepared with your self-assessment and any topics you'd like to discuss.

Best regards,
[Your Name]`,
  },
};

const GROUP_NAMES: Record<string, string> = {
  "1": "Engineering Team",
  "2": "Sales Department",
  "3": "HR Group",
};

export default function TemplatesPage() {
  const params = useParams();
  const router = useRouter();
  const groupId = params.groupId as string;
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);

  const templates = MOCK_TEMPLATES[groupId] || [];
  const groupName = GROUP_NAMES[groupId] || "Unknown Group";

  const handleTemplateClick = (e: React.MouseEvent, href: string) => {
    e.preventDefault();
    const templateId = href.replace("#", "");
    setSelectedTemplate(templateId);
  };

  const handleCustomize = () => {
    if (selectedTemplate) {
      router.push(`/dashboard?template=${selectedTemplate}`);
    }
  };

  const templateContent = selectedTemplate ? TEMPLATE_CONTENT[selectedTemplate] : null;

  return (
    <div className="min-h-screen bg-white pt-20">
      <div className="max-w-7xl mx-auto p-8">
        <div className="flex items-center gap-4 mb-8">
          <button
            onClick={() => router.push("/groups")}
            className="text-blue-600 hover:underline text-lg"
          >
            ← Back to Groups
          </button>
        </div>

        <h1 className="text-4xl font-bold mb-2 text-gray-900">{groupName}</h1>
        <p className="text-gray-600 text-lg mb-8">
          Select a template to preview and customize
        </p>

        <div onClick={(e) => {
          const target = e.target as HTMLElement;
          const link = target.closest("a");
          if (link) {
            handleTemplateClick(e, link.getAttribute("href") || "");
          }
        }}>
          <ResourceCardsGrid items={templates} />
        </div>
      </div>

      {/* Template Preview Modal */}
      {selectedTemplate && templateContent && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">Email Template Preview</h2>
              <button
                onClick={() => setSelectedTemplate(null)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X size={24} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6">
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 text-gray-900">
                  {templateContent.subject}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Body</label>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-gray-900 whitespace-pre-wrap font-mono text-sm">
                  {templateContent.body}
                </div>
              </div>
            </div>

            <div className="p-6 border-t border-gray-200 flex gap-4">
              <button
                onClick={() => setSelectedTemplate(null)}
                className="flex-1 bg-gray-100 text-gray-800 py-3 px-6 rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Close
              </button>
              <button
                onClick={handleCustomize}
                className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Customize Template
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
