// components/ui/resource-cards-grid.tsx

import * as React from "react";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/utils";

export interface ResourceCardItem {
  iconSrc: string;
  title: string;
  lastUpdated: string;
  href: string;
}

interface ResourceCardsGridProps {
  items: ResourceCardItem[];
  className?: string;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
  },
};

export const ResourceCardsGrid = ({ items, className }: ResourceCardsGridProps) => {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className={cn(
        "grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3",
        className
      )}
    >
      {items.map((item, index) => (
        <motion.a
          key={index}
          href={item.href}
          variants={itemVariants}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.98 }}
          className="group block"
        >
          <div className="flex h-full flex-col justify-between rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-shadow duration-300 hover:shadow-md">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-4">
                <img src={item.iconSrc} alt={`${item.title} icon`} className="h-10 w-10" />
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {item.title}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Last updated: {item.lastUpdated}
                  </p>
                </div>
              </div>
              <ArrowUpRight className="h-5 w-5 text-gray-600 transition-transform duration-300 group-hover:-translate-y-1 group-hover:translate-x-1" />
            </div>
          </div>
        </motion.a>
      ))}
    </motion.div>
  );
};
