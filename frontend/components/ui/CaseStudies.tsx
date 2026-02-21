"use client";

import React, { useEffect, useRef, useState } from "react";
import { Monitor, LayoutDashboard, Users } from "lucide-react";
import CountUp from "react-countup";

/** Hook: respects user's motion preferences */
function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined" || !("matchMedia" in window)) return;
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    setReduced(mq.matches);
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  return reduced;
}

/** Utility: parse a metric like "98%", "3.8x", "1.5M" */
function parseMetricValue(raw: string) {
  const value = (raw ?? "").toString().trim();
  const m = value.match(
    /^([^\d\-+]*?)\s*([\-+]?\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*([^\d\s]*)$/
  );
  if (!m) {
    return { prefix: "", end: 0, suffix: value, decimals: 0 };
  }
  const [, prefix, num, suffix] = m;
  const normalized = num.replace(/,/g, "");
  const end = parseFloat(normalized);
  const decimals = normalized.split(".")[1]?.length ?? 0;
  return {
    prefix: prefix ?? "",
    end: isNaN(end) ? 0 : end,
    suffix: suffix ?? "",
    decimals,
  };
}

interface MetricStatProps {
  value: string;
  label: string;
  sub?: string;
  duration?: number;
}

const MetricStat: React.FC<MetricStatProps> = ({
  value,
  label,
  sub,
  duration = 1.6,
}) => {
  const reduceMotion = usePrefersReducedMotion();
  const { prefix, end, suffix, decimals } = parseMetricValue(value);

  return (
    <div className="flex flex-col gap-2 text-left p-6">
      <p
        className="text-2xl font-medium text-gray-900 sm:text-4xl"
        aria-label={`${label} ${value}`}
      >
        {prefix}
        {reduceMotion ? (
          <span>
            {end.toLocaleString(undefined, {
              minimumFractionDigits: decimals,
              maximumFractionDigits: decimals,
            })}
          </span>
        ) : (
          <CountUp
            end={end}
            decimals={decimals}
            duration={duration}
            separator=","
            enableScrollSpy
            scrollSpyOnce
          />
        )}
        {suffix}
      </p>
      <p className="font-medium text-gray-900 text-left">{label}</p>
      {sub ? <p className="text-gray-600 text-left">{sub}</p> : null}
    </div>
  );
};

interface CaseStudy {
  id: number;
  quote: string;
  name: string;
  role: string;
  image: string;
  icon: React.ElementType;
  metrics: { value: string; label: string; sub: string }[];
}

const caseStudies: CaseStudy[] = [
  {
    id: 1,
    quote:
      "With CorpoMailer, our SDRs finally work in sync. Templates are shared, consistent, and we launch new campaigns 40% faster.",
    name: "Aarav Mehta",
    role: "Lead SDR",
    image:
      "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=1000&fit=crop",
    icon: Monitor,
    metrics: [
      { value: "40%", label: "Faster Launch", sub: "Campaign shipping speed" },
      { value: "95%", label: "Rep Satisfaction", sub: "Based on internal survey" },
    ],
  },
  {
    id: 2,
    quote:
      "CorpoMailer gave us a unified approval dashboard. Our ops team reduced risk and improved compliance across all outbound.",
    name: "Sophia Patel",
    role: "Campaign Ops Manager",
    image:
      "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800&h=1000&fit=crop",
    icon: LayoutDashboard,
    metrics: [
      { value: "3.5x", label: "Efficiency Gain", sub: "Across workflows" },
      { value: "70%", label: "Reduced Errors", sub: "In compliance reporting" },
    ],
  },
  {
    id: 3,
    quote:
      "The agentic features in CorpoMailer changed the way we scale. Everything is automated, and lead quality is higher.",
    name: "David Liu",
    role: "VP of Growth",
    image:
      "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=800&h=1000&fit=crop",
    icon: Users,
    metrics: [
      { value: "2x", label: "Lead Quality", sub: "Qualified pipeline" },
      {
        value: "88%",
        label: "Response Rate Boost",
        sub: "Teamwide adoption",
      },
    ],
  },
];

const CaseStudies: React.FC = () => {
  return (
    <section className="py-32 bg-white" aria-labelledby="case-studies-heading">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col gap-4 text-center max-w-2xl mx-auto">
          <h2
            id="case-studies-heading"
            className="text-4xl font-semibold md:text-5xl text-gray-900 tracking-tight"
          >
            Real results with Agents
          </h2>
          <p className="text-gray-500 text-lg">
            From automated research to strict governance—CorpoMailer powers
            teams with speed, clarity, and consistency.
          </p>
        </div>

        {/* Cases */}
        <div className="mt-20 flex flex-col gap-20">
          {caseStudies.map((study, idx) => {
            const reversed = idx % 2 === 1;
            return (
              <div
                key={study.id}
                className="grid gap-12 lg:grid-cols-3 xl:gap-24 items-center border-b border-gray-100 pb-12 last:border-0"
              >
                {/* Left: Image + Quote */}
                <div
                  className={[
                    "flex flex-col sm:flex-row gap-10 lg:col-span-2 lg:border-r lg:pr-12 xl:pr-16 text-left",
                    reversed
                      ? "lg:order-2 lg:border-r-0 lg:border-l border-gray-100 lg:pl-12 xl:pl-16 lg:pr-0"
                      : "border-gray-100",
                  ].join(" ")}
                >
                  <img
                    src={study.image}
                    alt={`${study.name} portrait`}
                    width={300}
                    height={400}
                    className="aspect-[29/35] h-auto w-full max-w-60 rounded-2xl object-cover ring-1 ring-gray-200 hover:scale-105 transition-all duration-300"
                    loading="lazy"
                    decoding="async"
                  />
                  <figure className="flex flex-col justify-between gap-8 text-left">
                    <blockquote className="text-lg sm:text-xl text-gray-900 leading-relaxed text-left">
                      <h3 className="text-lg sm:text-xl lg:text-xl font-normal text-gray-900 leading-relaxed text-left">
                        {study.quote}
                      </h3>
                    </blockquote>
                    <figcaption className="flex items-center gap-6 mt-4 text-left">
                      <div className="flex flex-col gap-1">
                        <span className="text-md font-medium text-gray-900">
                          {study.name}
                        </span>
                        <span className="text-sm text-gray-500">
                          {study.role}
                        </span>
                      </div>
                    </figcaption>
                  </figure>
                </div>

                {/* Right: Metrics */}
                <div
                  className={[
                    "grid grid-cols-1 gap-10 self-center text-left",
                    reversed ? "lg:order-1" : "",
                  ].join(" ")}
                >
                  {study.metrics.map((metric, i) => (
                    <MetricStat
                      key={`${study.id}-${i}`}
                      value={metric.value}
                      label={metric.label}
                      sub={metric.sub}
                    />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default CaseStudies;
