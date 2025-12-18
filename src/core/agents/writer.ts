import { BaseAgent } from './base-agent';
import { AgentRole, ProjectBrief, UiDesign } from '@/types';

export class ContentWriter extends BaseAgent {
  role: AgentRole = 'writer';
  name = "Content Writer";
  
  systemPrompt = \`You are a UX Copywriter.
  Generate professional content for the website based on the design.
  Output JSON format:
  {
    "hero_headline": "Main title",
    "hero_subheadline": "Subtitle",
    "cta_text": "Button text",
    "about_text": "Short about us paragraph",
    "features_content": [{"title": "...", "desc": "..."}]
  }\`;

  async writeContent(brief: ProjectBrief, design: UiDesign): Promise<any> {
    const context = \`Project: \${brief.summary}\nTarget Audience: \${brief.target_users}\`;
    return await this.askJson<any>("Write website copy.", context);
  }
}
