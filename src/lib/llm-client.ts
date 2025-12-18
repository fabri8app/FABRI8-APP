import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.OPENROUTER_API_KEY, 
  baseURL: "https://openrouter.ai/api/v1",
  dangerouslyAllowBrowser: true
});

export interface LLMParams {
  systemPrompt: string;
  userPrompt: string;
  temperature?: number;
  model?: string;
}

export async function callAgent(params: LLMParams): Promise<string> {
  try {
    const completion = await client.chat.completions.create({
      model: params.model || "google/gemini-2.0-flash-exp:free",
      messages: [
        { role: "system", content: params.systemPrompt },
        { role: "user", content: params.userPrompt }
      ],
      temperature: params.temperature || 0.7,
    });
    return completion.choices[0]?.message?.content || "";
  } catch (error) {
    console.error("AI Call Failed:", error);
    throw new Error("Failed to get response from Agent");
  }
}

export async function callAgentJson<T>(params: LLMParams): Promise<T> {
  const jsonSystemPrompt = \`\${params.systemPrompt}\n\nIMPORTANT: You must output ONLY valid JSON. Do not add markdown blocks.\`;
  
  const rawResponse = await callAgent({
    ...params,
    systemPrompt: jsonSystemPrompt,
    model: params.model || "google/gemini-2.0-flash-exp:free" 
  });

  try {
    const jsonStr = rawResponse.replace(/\`\`\`json/g, '').replace(/\`\`\`/g, '').trim();
    return JSON.parse(jsonStr) as T;
  } catch (e) {
    console.error("Failed to parse JSON from AI:", rawResponse);
    throw new Error("AI did not return valid JSON");
  }
}
