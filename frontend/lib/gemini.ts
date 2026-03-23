import { GoogleGenAI } from "@google/genai";

export type EmailTone = "Casual" | "Formal" | "Creative";

/** Lazy singleton – only constructed when actually needed (client-side) */
let aiClient: GoogleGenAI | null = null;

function getClient(): GoogleGenAI {
  if (!aiClient) {
    const apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY ?? "";
    aiClient = new GoogleGenAI({ apiKey });
  }
  return aiClient;
}

export const generateEmail = async (
  receiverName: string,
  senderName: string,
  companyName: string,
  context: string,
  tone: EmailTone
): Promise<string> => {
  try {
    const client = getClient();
    const prompt = `You are an AI assistant writing an email.
Sender: ${senderName}
Sender Company: ${companyName}
Receiver: ${receiverName}
Tone: ${tone}
Context: ${context}

Draft the email body. Do not include subject line or placeholders.`;

    const result = await client.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
    });

    return result.text ?? "Could not generate email.";
  } catch (clientError) {
    console.error("Client-side generation failed:", clientError);
    throw new Error("Failed to generate email.");
  }
};
