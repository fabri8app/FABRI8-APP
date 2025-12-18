import { BaseAgent } from './base-agent';
import { AgentRole, CodeFile } from '@/types';

export class DebuggerAgent extends BaseAgent {
  role: AgentRole = 'debugger';
  name = "Debugger & DevOps";
  
  systemPrompt = \`You are an expert Debugger. Fix the code based on issues found.
  Return the FULL fixed code files.
  Output JSON:
  {
    "fixed_files": [
      { "path": "...", "content": "...", "language": "..." }
    ]
  }\`;

  async fixBugs(code: CodeFile[], issues: any[]): Promise<CodeFile[]> {
    const issueText = JSON.stringify(issues);
    const response = await this.askJson<{fixed_files: CodeFile[]}>("Fix these issues in the code.", issueText);
    return response.fixed_files;
  }
}
