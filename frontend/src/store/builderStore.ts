/**
 * Builder State Management (Zustand)
 */

import { create } from 'zustand';
import type { Agent, AgentRole, AgentStatus } from '@/types/agent';

interface BuilderState {
  // Workflow
  currentPhase: number;
  totalPhases: number;
  isGenerating: boolean;
  
  // Agents
  agents: Record<AgentRole, Agent>;
  
  // Output
  generatedCode: {
    html: string;
    css: string;
    js: string;
  };
  
  // Project
  projectId: string | null;
  projectName: string;
  
  // Actions
  setPhase: (phase: number) => void;
  updateAgent: (role: AgentRole, update: Partial<Agent>) => void;
  setGeneratedCode: (code: BuilderState['generatedCode']) => void;
  setGenerating: (isGenerating: boolean) => void;
  setProjectId: (id: string) => void;
  reset: () => void;
}

const initialAgents: Record<AgentRole, Agent> = {
  pm: { name: 'Project Manager', role: 'pm', status: 'idle', progress: 0, message: '' },
  ui: { name: 'UI/UX Designer', role: 'ui', status: 'idle', progress: 0, message: '' },
  frontend: { name: 'Frontend Dev', role: 'frontend', status: 'idle', progress: 0, message: '' },
  backend: { name: 'Backend Dev', role: 'backend', status: 'idle', progress: 0, message: '' },
  writer: { name: 'Content Writer', role: 'writer', status: 'idle', progress: 0, message: '' },
  reviewer: { name: 'Code Reviewer', role: 'reviewer', status: 'idle', progress: 0, message: '' },
  qa: { name: 'QA Tester', role: 'qa', status: 'idle', progress: 0, message: '' },
  debugger: { name: 'Debugger', role: 'debugger', status: 'idle', progress: 0, message: '' }
};

export const useBuilderStore = create<BuilderState>((set) => ({
  currentPhase: 0,
  totalPhases: 7,
  isGenerating: false,
  agents: initialAgents,
  generatedCode: { html: '', css: '', js: '' },
  projectId: null,
  projectName: 'Untitled Project',
  
  setPhase: (phase) => set({ currentPhase: phase }),
  
  updateAgent: (role, update) => set((state) => ({
    agents: {
      ...state.agents,
      [role]: { ...state.agents[role], ...update }
    }
  })),
  
  setGeneratedCode: (code) => set({ generatedCode: code }),
  
  setGenerating: (isGenerating) => set({ isGenerating }),
  
  setProjectId: (id) => set({ projectId: id }),
  
  reset: () => set({
    currentPhase: 0,
    isGenerating: false,
    agents: initialAgents,
    generatedCode: { html: '', css: '', js: '' },
    projectId: null
  })
}));
