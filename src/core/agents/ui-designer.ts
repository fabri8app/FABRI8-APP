import { BaseAgent } from './base-agent';
import { AgentRole, UiDesign, ProjectBrief } from '@/types';

export class UiDesigner extends BaseAgent {
  role: AgentRole = 'ui';
  name = "UI/UX Designer";
  
  systemPrompt = \`You are a creative UI/UX Designer.
  Design the visual structure based on the Project Brief.
  Output Format JSON:
  {
    "layout": "Description of layout",
    "colors": ["#hex", "#hex"],
    "typography": "Font recommendations",
    "components": ["List of components needed e.g. Header, Hero"]
  }\`;

  async createDesign(brief: ProjectBrief): Promise<UiDesign> {
    const context = \`Summary: \${brief.summary}\nKey Features: \${brief.key_features.join(', ')}\`;
    return await this.askJson<UiDesign>("Create a UI Design System.", context);
  }
}
