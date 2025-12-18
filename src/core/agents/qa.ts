import { BaseAgent } from './base-agent';
import { AgentRole, QaReport } from '@/types';

export class QaTester extends BaseAgent {
  role: AgentRole = 'qa';
  name = "QA Engineer";
  
  systemPrompt = \`You are a QA Engineer. Simulate testing of the application.
  Output JSON:
  {
    "status": "PASS" | "FAIL",
    "bugs": [{"severity": "high", "issue": "...", "suggestion": "..."}]
  }\`;

  async test(frontend: any[], backend: any[]): Promise<QaReport> {
    return await this.askJson<QaReport>("Simulate testing scenarios and report bugs.");
  }
}
