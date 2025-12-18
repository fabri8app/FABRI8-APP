/**
 * Agent Status Display Component
 */

'use client';

import { useBuilderStore } from '@/store/builderStore';
import { AGENT_INFO } from '@/types/agent';
import type { AgentRole } from '@/types/agent';

export function AgentStatus() {
  const agents = useBuilderStore((state) => state.agents);

  const agentRoles: AgentRole[] = ['pm', 'ui', 'frontend', 'backend', 'writer', 'reviewer', 'qa', 'debugger'];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {agentRoles.map((role) => {
        const agent = agents[role];
        const info = AGENT_INFO[role];
        const statusColors = {
          idle: 'bg-gray-100 text-gray-600',
          working: 'bg-blue-100 text-blue-600 animate-pulse',
          completed: 'bg-green-100 text-green-600',
          error: 'bg-red-100 text-red-600'
        };

        return (
          <div
            key={role}
            className={`p-4 rounded-lg ${statusColors[agent.status]} transition`}
          >
            <div className="text-2xl mb-2">{info.emoji}</div>
            <div className="text-sm font-semibold">{info.name}</div>
            <div className="text-xs mt-1">
              {agent.status === 'working' && '⏳ Working...'}
              {agent.status === 'completed' && '✅ Done'}
              {agent.status === 'idle' && '⏸️ Idle'}
              {agent.status === 'error' && '❌ Error'}
            </div>
            {agent.progress > 0 && (
              <div className="w-full bg-gray-200 rounded-full h-1 mt-2">
                <div
                  className="bg-current h-1 rounded-full"
                  style={{ width: `${agent.progress}%` }}
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
