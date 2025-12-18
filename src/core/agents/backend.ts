import { BaseAgent } from './base-agent';
import { AgentRole, ProjectBrief, CodeFile } from '@/types';

export class BackendDev extends BaseAgent {
  role: AgentRole = 'backend';
  name = "Backend Developer";
  
  systemPrompt = \`You are a Senior Backend Developer using Next.js API Routes.
  Create API endpoints with MOCK DATA.
  Output Format JSON:
  {
    "files": [
      { "path": "src/app/api/users/route.ts", "content": "...", "language": "typescript" }
    ]
  }\`;

  async generateAPIs(brief: ProjectBrief): Promise<CodeFile[]> {
    const context = \`Project: \${brief.summary}\nFeatures: \${brief.key_features.join(', ')}\`;
    const response = await this.askJson<{ files: CodeFile[] }>("Generate API routes with mock data.", context);
    return response.files;
  }
}
