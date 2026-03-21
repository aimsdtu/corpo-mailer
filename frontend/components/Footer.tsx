"use client";

import React from "react";
import Link from "next/link";
import { Twitter, Github, Linkedin } from "lucide-react";

const footerSections = [
  {
    title: "Platform",
    links: ["Features", "AI Agents", "Pricing", "Changelog", "Roadmap"],
  },
  {
    title: "Solutions",
    links: ["For Sales", "For Recruiting", "For Founders", "Enterprise"],
  },
  {
    title: "Resources",
    links: ["About", "Blog", "Docs", "Help Center", "Community"],
  },
  {
    title: "Company",
    links: ["About Us", "Contact Us", "Careers", "Partners"],
  },
  {
    title: "Legal",
    links: ["Privacy", "Terms", "Security", "GDPR"],
  },
];

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 pt-16 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-7 gap-8 mb-12">
          <div className="col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-6">
              <div className="w-8 h-8 bg-black text-white rounded-lg flex items-center justify-center font-bold text-xl tracking-tighter">
                CM
              </div>
              <span className="font-bold text-xl tracking-tight">
                corpomailer.com
              </span>
            </Link>
            <p className="text-gray-500 text-sm mb-6 max-w-xs">
              Automate the T&P Cell&apos;s entire placement outreach. Built for
              high-volume, personalized outreach with strict governance.
            </p>
            <div className="flex gap-4">
              <a
                href="#"
                className="text-gray-400 hover:text-black transition-colors"
                aria-label="Twitter"
              >
                <Twitter size={20} />
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-black transition-colors"
                aria-label="GitHub"
              >
                <Github size={20} />
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-black transition-colors"
                aria-label="LinkedIn"
              >
                <Linkedin size={20} />
              </a>
            </div>
          </div>

          {footerSections.map((section) => (
            <div key={section.title} className="col-span-1">
              <h4 className="font-semibold text-gray-900 mb-4">
                {section.title}
              </h4>
              <ul className="space-y-3">
                {section.links.map((link) => (
                  <li key={link}>
                    {link === "About Us" ? (
                      <Link
                        href="/about"
                        className="text-sm text-gray-500 hover:text-black transition-colors"
                      >
                        {link}
                      </Link>
                    ) : link === "Contact Us" ? (
                      <Link
                        href="/contact"
                        className="text-sm text-gray-500 hover:text-black transition-colors"
                      >
                        {link}
                      </Link>
                    ) : (
                      <a
                        href="#"
                        className="text-sm text-gray-500 hover:text-black transition-colors"
                      >
                        {link}
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="pt-8 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-gray-400">
            © {new Date().getFullYear()} CorpoMailer, Inc. All rights reserved.
          </p>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500" />
            <span className="text-sm text-gray-500 font-medium">
              All agents operational
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
