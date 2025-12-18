import { BaseAgent } from './base-agent';
import { AgentRole, UiDesign, ProjectBrief, CodeFile } from '@/types';

export class FrontendDev extends BaseAgent {
  role: AgentRole = 'frontend';
  name = "Frontend Developer";
  
  systemPrompt = \`You are an expert Frontend Developer using Next.js 14, Tailwind CSS, and Lucide React.
  Generate code based on the Design System.
  RULES:
  1. Use 'use client' where needed.
  2. Output MUST be valid JSON array of files.
  Output Format JSON:
  {
    "files": [
      { "path": "src/components/Hero.tsx", "content": "...", "language": "typescript" }
    ]
  }\`;

  async generateCode(brief: ProjectBrief, design: UiDesign): Promise<CodeFile[]> {
    const context = \`Project: \${brief.summary}\nDesign: \${design.layout}\nComponents: \${design.components.join(', ')}\`;
    const response = await this.askJson<{ files: CodeFile[] }>("Generate frontend code.", context);
    return response.files;
  }
}
