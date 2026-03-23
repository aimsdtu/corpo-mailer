// Simple mock store to simulate a database for the demo

export interface EmailJob {
  id: string;
  senderName: string;
  receiverName: string;
  receiverEmail: string;
  subject: string;
  body: string;
  status: "pending" | "approved" | "rejected" | "sent";
  tone: string;
  timestamp: string;
}

const STORAGE_KEY = "corpomailer_jobs";

export const getJobs = (): EmailJob[] => {
  if (typeof window === "undefined") return [];
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? (JSON.parse(stored) as EmailJob[]) : [];
};

export const addJob = (
  job: Omit<EmailJob, "id" | "status" | "timestamp">
): EmailJob => {
  const jobs = getJobs();
  const newJob: EmailJob = {
    ...job,
    id: Math.random().toString(36).substring(2, 9),
    status: "pending",
    timestamp: new Date().toISOString(),
  };
  jobs.unshift(newJob);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(jobs));
  return newJob;
};

export const updateJobStatus = (id: string, status: EmailJob["status"]) => {
  const jobs = getJobs();
  const updatedJobs = jobs.map((job) =>
    job.id === id ? { ...job, status } : job
  );
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedJobs));
};

export const deleteJob = (id: string) => {
  const jobs = getJobs();
  const updatedJobs = jobs.filter((job) => job.id !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedJobs));
};
