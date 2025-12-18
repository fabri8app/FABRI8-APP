import { callAgent, callAgentJson, LLMParams } from '@/lib/llm-client';
import { AgentRole } from '@/types';

export abstract class BaseAgent {
  abstract role: AgentRole;
  abstract name: string;
  abstract systemPrompt: string;

  async ask(userPrompt: string, context: string = ""): Promise<string> {
    const fullPrompt = context ? \`Context:\n\${context}\n\nTask: \${userPrompt}\` : userPrompt;
    console.log(\`🤖 [\${this.name}] Working...\`);
    return await callAgent({
      systemPrompt: this.systemPrompt,
      userPrompt: fullPrompt,
      temperature: 0.7
    });
  }

  async askJson<T>(userPrompt: string, context: string = ""): Promise<T> {
    const fullPrompt = context ? \`Context:\n\${context}\n\nTask: \${userPrompt}\` : userPrompt;
    console.log(\`🤖 [\${this.name}] Working on JSON...\`);
    return await callAgentJson<T>({
      systemPrompt: this.systemPrompt,
      userPrompt: fullPrompt,
      temperature: 0.2
    });
  }
}
