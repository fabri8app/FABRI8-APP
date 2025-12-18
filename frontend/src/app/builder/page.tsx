/**
 * Builder Page
 */

'use client';

import { useState, useEffect } from 'react';
import { PromptInput } from '@/components/builder/PromptInput';
import { AgentStatus } from '@/components/builder/AgentStatus';
import { useBuilderStore } from '@/store/builderStore';

export default function BuilderPage() {
  const [isLoading, setIsLoading] = useState(false);
  const { setGenerating, updateAgent, setProjectId, setGeneratedCode } = useBuilderStore();

  useEffect(() => {
    // Setup WebSocket connection for real-time updates
    const ws = new WebSocket(process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8001');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.agent && data.status) {
        updateAgent(data.agent, {
          status: data.status,
          message: data.message,
          progress: data.progress || 0
        });
      }
      
      if (data.generated_code) {
        setGeneratedCode(data.generated_code);
      }
    };

    return () => ws.close();
  }, []);

  const handleGenerateWebsite = async (prompt: string) => {
    try {
      setIsLoading(true);
      setGenerating(true);

      const response = await fetch('/api/builder/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });

      const data = await response.json();
      
      if (data.project_id) {
        setProjectId(data.project_id);
      }
      
      if (data.code) {
        setGeneratedCode(data.code);
      }
    } catch (error) {
      console.error('Generation error:', error);
      alert('Failed to generate website');
    } finally {
      setIsLoading(false);
      setGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🔥 FABRI8 Builder
          </h1>
          <p className="text-gray-600">
            AI-powered website generation with 8 specialized agents
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Section */}
          <div className="lg:col-span-1 bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold mb-6">Create Your Website</h2>
            <PromptInput onSubmit={handleGenerateWebsite} isLoading={isLoading} />
          </div>

          {/* Agents Section */}
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold mb-6">Agent Status</h2>
            <AgentStatus />
          </div>
        </div>
      </div>
    </div>
  );
}
