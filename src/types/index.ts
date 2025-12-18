export interface ProjectState {
  step: 'discovery' | 'design' | 'implementation' | 'review' | 'testing' | 'complete';
  projectBrief: ProjectBrief | null;
  uiDesign: UiDesign | null;
  architecture: {
    frontend: FrontendArch | null;
    backend: BackendArch | null;
  };
  code: {
    frontend: CodeFile[];
    backend: CodeFile[];
  };
  content: Record<string, string>;
  qaReport: QaReport | null;
}

export interface ProjectBrief {
  summary: string;
  target_users: string;
  key_features: string[];
  tech_stack: string;
}

export interface UiDesign {
  layout: string;
  colors: string[];
  typography: string;
  components: string[];
}

export interface FrontendArch {
  components_structure: string[];
  state_management: string;
  api_integrations: string[];
}

export interface BackendArch {
  endpoints: Array<{ method: string; path: string; purpose: string }>;
  database_schema: Record<string, string[]>;
}

export interface CodeFile {
  path: string;
  content: string;
  language: 'typescript' | 'python' | 'css' | 'json';
}

export interface QaReport {
  status: 'PASS' | 'FAIL';
  bugs: Array<{ severity: 'high' | 'medium' | 'low'; issue: string; suggestion: string; }>;
}

export type AgentRole = 'pm' | 'ui' | 'frontend' | 'backend' | 'writer' | 'reviewer' | 'qa' | 'debugger';

export interface AgentResponse {
  role: AgentRole;
  content: string;
  data?: any;
}
