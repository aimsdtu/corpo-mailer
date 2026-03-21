import * as React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { cva } from "class-variance-authority";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Check, X } from "lucide-react";

interface Contributor {
  src: string;
  alt: string;
  fallback: string;
}

type StatusVariant = "pending" | "approved" | "rejected";

export interface GroupRequest {
  id: string;
  groupName: string;
  userName: string;
  userEmail: string;
  requestDate: string;
  contributors: Contributor[];
  status: {
    text: string;
    variant: StatusVariant;
  };
}

interface GroupDataTableProps {
  requests: GroupRequest[];
  visibleColumns: Set<keyof GroupRequest>;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}

const badgeVariants = cva("capitalize text-white", {
  variants: {
    variant: {
      pending: "bg-yellow-500 hover:bg-yellow-600",
      approved: "bg-green-500 hover:bg-green-600",
      rejected: "bg-red-500 hover:bg-red-600",
    },
  },
  defaultVariants: {
    variant: "pending",
  },
});

export const GroupDataTable = ({ requests, visibleColumns, onApprove, onReject }: GroupDataTableProps) => {
  const rowVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.05,
        duration: 0.3,
        ease: "easeInOut",
      },
    }),
  };
  
  const tableHeaders: { key: keyof GroupRequest; label: string }[] = [
    { key: "groupName", label: "Group" },
    { key: "userName", label: "User" },
    { key: "userEmail", label: "Email" },
    { key: "requestDate", label: "Request Date" },
    { key: "contributors", label: "Members" },
    { key: "status", label: "Status" },
  ];

  return (
    <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
      <div className="relative w-full overflow-auto">
        <Table>
          <TableHeader>
            <TableRow>
              {tableHeaders
                .filter((header) => visibleColumns.has(header.key))
                .map((header) => (
                  <TableHead key={header.key}>{header.label}</TableHead>
                ))}
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {requests.length > 0 ? (
              requests.map((request, index) => (
                <motion.tr
                  key={request.id}
                  custom={index}
                  initial="hidden"
                  animate="visible"
                  variants={rowVariants}
                  className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
                >
                  {visibleColumns.has("groupName") && <TableCell className="font-medium">{request.groupName}</TableCell>}
                  {visibleColumns.has("userName") && <TableCell>{request.userName}</TableCell>}
                  {visibleColumns.has("userEmail") && <TableCell>{request.userEmail}</TableCell>}
                  {visibleColumns.has("requestDate") && <TableCell>{request.requestDate}</TableCell>}
                  
                  {visibleColumns.has("contributors") && (
                    <TableCell>
                      <div className="flex -space-x-2">
                        {request.contributors.map((contributor, idx) => (
                          <Avatar key={idx} className="h-8 w-8 border-2 border-background">
                            <AvatarImage src={contributor.src} alt={contributor.alt} />
                            <AvatarFallback>{contributor.fallback}</AvatarFallback>
                          </Avatar>
                        ))}
                      </div>
                    </TableCell>
                  )}

                  {visibleColumns.has("status") && (
                    <TableCell>
                      <Badge className={cn(badgeVariants({ variant: request.status.variant }))}>
                        {request.status.text}
                      </Badge>
                    </TableCell>
                  )}

                  <TableCell>
                    {request.status.variant === "pending" && (
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          onClick={() => onApprove(request.id)}
                          className="bg-green-600 hover:bg-green-700"
                        >
                          <Check className="h-4 w-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => onReject(request.id)}
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    )}
                  </TableCell>
                </motion.tr>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={visibleColumns.size + 1} className="h-24 text-center">
                  No requests.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};
