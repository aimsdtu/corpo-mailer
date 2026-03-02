/**
 * Typed API functions for auth & user endpoints.
 */
import { apiFetch } from "./client";
import type { TokenResponse, User } from "@/lib/auth/store";
/* ------------------------------------------------------------------ */
/*  Groups                                                             */
/* ------------------------------------------------------------------ */

export interface Group {
  uuid: string;
  name: string;
  bio?: string | null;
  created_by: string;
  created_at: string;
}

export interface GroupMember {
  user_id: string;
  role: string;
  joined_at: string;
}

export interface CreateGroupPayload {
  name: string;
  bio?: string;
}

/* ------------------------------------------------------------------ */
/*  Auth                                                               */
/* ------------------------------------------------------------------ */

export interface RegisterPayload {
  email: string;
  password: string;
  name: string;
}

export async function register(payload: RegisterPayload) {
  return apiFetch<TokenResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function login(email: string, password: string) {
  return apiFetch<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function googleLoginRedirect() {
  // Backend returns a 302 redirect — navigate directly
  window.location.href = "/api/v1/auth/login/google";
}

export async function refresh() {
  return apiFetch<{ access_token: string; token_type: string }>("/auth/refresh", {
    method: "POST",
  });
}

export async function logout() {
  return apiFetch<void>("/auth/logout", { method: "POST" });
}

export async function me() {
  return apiFetch<{ sub: string; role: string; provider: string; email: string }>("/auth/me");
}

/* ------------------------------------------------------------------ */
/*  Users                                                              */
/* ------------------------------------------------------------------ */

export async function getUser(uuid: string) {
  return apiFetch<User>(`/users/${uuid}`);
}

export async function listUsers(params?: {
  designation?: string;
  access_level?: string;
  limit?: number;
  offset?: number;
}) {
  const qs = new URLSearchParams();
  if (params?.designation) qs.set("designation", params.designation);
  if (params?.access_level) qs.set("access_level", params.access_level);
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  const suffix = qs.toString() ? `?${qs}` : "";
  return apiFetch<User[]>(`/users${suffix}`);
}

export async function deleteUser(uuid: string) {
  return apiFetch<void>(`/users/${uuid}`, { method: "DELETE" });
}

export async function updatePassword(uuid: string, oldPassword: string, newPassword: string) {
  return apiFetch<void>(`/users/${uuid}/password`, {
    method: "PUT",
    body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
  });
}

export async function countUsers(params?: { designation?: string; access_level?: string }) {
  const qs = new URLSearchParams();
  if (params?.designation) qs.set("designation", params.designation);
  if (params?.access_level) qs.set("access_level", params.access_level);
  const suffix = qs.toString() ? `?${qs}` : "";
  return apiFetch<{ count: number }>(`/users/count${suffix}`);
}
/* ------------------------------------------------------------------ */
/*  Groups                                                             */
/* ------------------------------------------------------------------ */

export async function createGroup(payload: CreateGroupPayload) {
  return apiFetch<Group>("/groups", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listGroups() {
  return apiFetch<Group[]>("/groups");
}

export async function getGroup(groupId: string) {
  return apiFetch<Group>(`/groups/${groupId}`);
}

export async function deleteGroup(groupId: string) {
  return apiFetch<void>(`/groups/${groupId}`, {
    method: "DELETE",
  });
}

export async function myGroups() {
  return apiFetch<Group[]>("/groups/me/groups");
}

/* ---------------- Members ---------------- */

export async function addMember(groupId: string, userId: string) {
  return apiFetch<void>(
    `/groups/${groupId}/members/${userId}`,
    {
      method: "POST",
    },
  );
}

export async function removeMember(groupId: string, userId: string) {
  return apiFetch<void>(
    `/groups/${groupId}/members/${userId}`,
    {
      method: "DELETE",
    },
  );
}

export async function updateMemberRole(
  groupId: string,
  userId: string,
  role: string,
) {
  return apiFetch<void>(
    `/groups/${groupId}/members/${userId}/role`,
    {
      method: "PATCH",
      body: JSON.stringify({ role }),
    },
  );
}

export async function listMembers(groupId: string) {
  return apiFetch<GroupMember[]>(
    `/groups/${groupId}/members`,
  );
}
/* ------------------------------------------------------------------ */
/*  Mails                                                              */
/* ------------------------------------------------------------------ */

export interface MailResponse {
  uuid: string;
  subject: string;
  body: string;
  llm_body?: string | null;
  group_id: string;
  created_by: string;
  status: string;
  template_id?: string | null;
  created_at: string;
  updated_at: string;
}

export interface MailCreate {
  subject: string;
  body: string;
  llm_body?: string | null;
  group_id: string;
  template_id?: string | null;
}

export interface MailUpdate {
  subject?: string;
  body?: string;
  llm_body?: string | null;
}

export interface MailDiffResponse {
  uuid: string;
  mail_id: string;
  changed_by: string;
  changed_at: string;
  old_body: string;
  new_body: string;
}

export async function createMail(payload: MailCreate) {
  return apiFetch<MailResponse>("/mails", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getMail(mailId: string) {
  return apiFetch<MailResponse>(`/mails/${mailId}`);
}

export async function listMails() {
  return apiFetch<MailResponse[]>("/mails");
}

export async function listGroupMails(groupId: string) {
  return apiFetch<MailResponse[]>(`/mails/groups/${groupId}`);
}

export async function updateMail(mailId: string, payload: MailUpdate) {
  return apiFetch<MailResponse>(`/mails/${mailId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function submitMail(mailId: string) {
  return apiFetch<MailResponse>(`/mails/${mailId}/submit`, {
    method: "POST",
  });
}

export async function approveMail(mailId: string) {
  return apiFetch<MailResponse>(`/mails/${mailId}/approve`, {
    method: "POST",
  });
}

export async function rejectMail(mailId: string) {
  return apiFetch<MailResponse>(`/mails/${mailId}/reject`, {
    method: "POST",
  });
}

export async function sendMail(mailId: string) {
  return apiFetch<MailResponse>(`/mails/${mailId}/send`, {
    method: "POST",
  });
}

export async function getMailDiffs(mailId: string) {
  return apiFetch<MailDiffResponse[]>(`/mails/${mailId}/diffs`);
}

export async function deleteMail(mailId: string) {
  return apiFetch<void>(`/mails/${mailId}`, {
    method: "DELETE",
  });
}

/* ------------------------------------------------------------------ */
/*  Templates                                                          */
/* ------------------------------------------------------------------ */

export interface TemplateResponse {
  uuid: string;
  name: string;
  content: string;
  group_id: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface TemplateCreate {
  name: string;
  content: string;
  group_id: string;
}

export interface TemplateUpdate {
  name?: string;
  content?: string;
}

export async function createTemplate(payload: TemplateCreate) {
  return apiFetch<TemplateResponse>("/templates", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getTemplate(templateId: string) {
  return apiFetch<TemplateResponse>(`/templates/${templateId}`);
}

export async function listTemplates(groupId?: string) {
  const qs = groupId ? `?group_id=${groupId}` : "";
  return apiFetch<TemplateResponse[]>(`/templates${qs}`);
}

export async function updateTemplate(templateId: string, payload: TemplateUpdate) {
  return apiFetch<TemplateResponse>(`/templates/${templateId}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function deleteTemplate(templateId: string) {
  return apiFetch<void>(`/templates/${templateId}`, {
    method: "DELETE",
  });
}