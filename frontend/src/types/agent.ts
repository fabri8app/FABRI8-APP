/**
 * Agent Type Definitions
 */

export type AgentRole = 
  | 'pm'
  | 'ui'
  | 'frontend'
  | 'backend'
  | 'writer'
  | 'reviewer'
  | 'qa'
  | 'debugger';

export type AgentStatus = 'idle' | 'working' | 'completed' | 'error';

export interface Agent {
  name: string;
  role: AgentRole;
  status: AgentStatus;
  progress: number;
  message: string;
  output?: Record<string, any>;
}

export interface AgentOutput {
  agent: string;
  role: AgentRole;
  output: Record<string, any>;
  status: 'completed' | 'error';
  error?: string;
}

export const AGENT_INFO: Record<AgentRole, { name: string; emoji: string; color: string }> = {
  pm: { name: 'Project Manager', emoji: '📊', color: 'blue' },
  ui: { name: 'UI/UX Designer', emoji: '🎨', color: 'purple' },
  frontend: { name: 'Frontend Dev', emoji: '💻', color: 'green' },
  backend: { name: 'Backend Dev', emoji: '⚙️', color: 'orange' },
  writer: { name: 'Content Writer', emoji: '✍️', color: 'pink' },
  reviewer: { name: 'Code Reviewer', emoji: '👀', color: 'red' },
  qa: { name: 'QA Tester', emoji: '🧪', color: 'cyan' },
  debugger: { name: 'Debugger', emoji: '🐛', color: 'yellow' }
};
