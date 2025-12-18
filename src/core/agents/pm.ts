import { BaseAgent } from './base-agent';
import { AgentRole, ProjectBrief } from '@/types';

export class ProjectManager extends BaseAgent {
  role: AgentRole = 'pm';
  name = "Project Manager";
  
  systemPrompt = \`You are an expert Senior Project Manager.
  Analyze user requests and break them down into a clear Project Brief.
  DO NOT write code. Define WHAT needs to be built.
  Output Format JSON:
  {
    "summary": "One sentence summary",
    "target_users": "Target audience",
    "key_features": ["Feature 1", "Feature 2"],
    "tech_stack": "Suggested stack"
  }\`;

  async analyze(userPrompt: string): Promise<ProjectBrief> {
    return await this.askJson<ProjectBrief>(
      \`Create a project brief for: "\${userPrompt}"\`
    );
  }
}
