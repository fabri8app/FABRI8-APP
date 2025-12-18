import { BaseAgent } from './base-agent';
import { AgentRole, CodeFile } from '@/types';

export class CodeReviewer extends BaseAgent {
  role: AgentRole = 'reviewer';
  name = "Senior Code Reviewer";
  
  systemPrompt = \`You are a Senior Developer. Review the code for errors, security, and best practices.
  Output JSON:
  {
    "score": 85,
    "issues": [
      {"severity": "high", "file": "filename", "issue": "description", "suggestion": "fix"}
    ]
  }\`;

  async reviewCode(frontend: CodeFile[], backend: CodeFile[]): Promise<any> {
    const codeSummary = frontend.map(f => \`File: \${f.path}\nCode:\n\${f.content.substring(0, 500)}...\`).join('\n');
    return await this.askJson<any>("Review this code.", codeSummary);
  }
}
