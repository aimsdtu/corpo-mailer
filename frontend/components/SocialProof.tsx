"use client";

import React from "react";

const logos = ["Oracle", "Salesforce", "HubSpot", "Outreach", "ZoomInfo"];

const SocialProof: React.FC = () => {
  return (
    <section className="py-12 border-y border-gray-100 bg-gray-50/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm font-medium text-gray-500 mb-8">
          TRUSTED BY 10,000+ OUTREACH TEAMS AT
        </p>
        <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 grayscale opacity-60">
          {logos.map((name) => (
            <div
              key={name}
              className="text-xl font-bold text-gray-400 font-mono select-none"
            >
              {name}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SocialProof;
