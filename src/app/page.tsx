'use client';

import { useState } from 'react';
import { Bot, Code2, Layers, Play, Loader2, CheckCircle2 } from 'lucide-react';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('Ready');
  const [result, setResult] = useState<any>(null);

  const handleGenerate = async () => {
    if (!prompt) return;
    
    setLoading(true);
    setStatus('Initializing Team...');
    setResult(null);

    try {
      // Fake progress updates (kyunki real backend ek baar me response deta hai)
      // Ye user ko feel dega ki agents kaam kar rahe hain
      setTimeout(() => setStatus('Phase 1: PM Analyzing Requirements...'), 1000);
      setTimeout(() => setStatus('Phase 2: UI Designer Creating Layouts...'), 3000);
      setTimeout(() => setStatus('Phase 3: Dev Team Coding (Parallel)...'), 6000);

      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      
      setStatus('Complete!');
      setResult(data);
    } catch (error) {
      console.error(error);
      setStatus('Error Occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex h-screen bg-darker text-white overflow-hidden">
      {/* Sidebar - Controls */}
      <div className="w-1/3 border-r border-gray-800 p-6 flex flex-col">
        <h1 className="text-2xl font-bold mb-6 flex items-center gap-2 text-blue-400">
          <Bot className="w-8 h-8" /> Fabri8 Agents
        </h1>
        
        <div className="flex-1 flex flex-col gap-4">
          <label className="text-sm text-gray-400">What do you want to build?</label>
          <textarea 
            className="w-full h-40 bg-gray-900 border border-gray-700 rounded-lg p-4 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
            placeholder="E.g., A portfolio website for a photographer with a dark theme and gallery..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          
          <button 
            onClick={handleGenerate}
            disabled={loading || !prompt}
            className={`flex items-center justify-center gap-2 p-4 rounded-lg font-bold transition-all ${
              loading ? 'bg-blue-900/50 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500'
            }`}
          >
            {loading ? <Loader2 className="animate-spin" /> : <Play size={20} />}
            {loading ? 'Agents Working...' : 'Start Building'}
          </button>

          {/* Status Monitor */}
          <div className="mt-8 p-4 bg-gray-900 rounded-lg border border-gray-800">
            <h3 className="text-sm font-semibold text-gray-400 mb-3 uppercase tracking-wider">Live Status</h3>
            <div className="flex items-center gap-3 text-blue-300">
              {loading && <Loader2 className="w-4 h-4 animate-spin" />}
              {!loading && result && <CheckCircle2 className="w-4 h-4 text-green-500" />}
              <span>{status}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Area - Results */}
      <div className="flex-1 bg-dark p-8 overflow-y-auto">
        {!result && (
          <div className="h-full flex flex-col items-center justify-center text-gray-500 opacity-50">
            <Layers size={64} strokeWidth={1} />
            <p className="mt-4">Waiting for inputs...</p>
          </div>
        )}

        {result && (
          <div className="space-y-8 animate-in fade-in duration-500">
            {/* PM Section */}
            <div className="border border-gray-700 rounded-xl overflow-hidden">
              <div className="bg-gray-800 p-4 border-b border-gray-700 font-bold flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-purple-500"></span> Project Manager Brief
              </div>
              <div className="p-4 bg-gray-900/50">
                <p className="text-gray-300 mb-2">{result.finalState.projectBrief.summary}</p>
                <div className="flex gap-2 flex-wrap">
                  {result.finalState.projectBrief.key_features.map((f: any, i: number) => (
                    <span key={i} className="px-2 py-1 bg-purple-900/30 text-purple-300 text-xs rounded border border-purple-800">
                      {f}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* UI Section */}
            <div className="border border-gray-700 rounded-xl overflow-hidden">
              <div className="bg-gray-800 p-4 border-b border-gray-700 font-bold flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-pink-500"></span> UI Design System
              </div>
              <div className="p-4 bg-gray-900/50 grid grid-cols-2 gap-4">
                 <div>
                    <h4 className="text-xs text-gray-500 uppercase mb-1">Layout</h4>
                    <p className="text-sm">{result.finalState.uiDesign.layout}</p>
                 </div>
                 <div>
                    <h4 className="text-xs text-gray-500 uppercase mb-1">Colors</h4>
                    <div className="flex gap-2">
                      {result.finalState.uiDesign.colors.map((c: string, i: number) => (
                        <div key={i} className="w-6 h-6 rounded-full border border-gray-600" style={{background: c}} title={c}></div>
                      ))}
                    </div>
                 </div>
              </div>
            </div>

            {/* Code Section */}
            <div className="border border-gray-700 rounded-xl overflow-hidden">
              <div className="bg-gray-800 p-4 border-b border-gray-700 font-bold flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-500"></span> Generated Code
                <span className="ml-auto text-xs bg-green-900 text-green-300 px-2 py-1 rounded">
                   {result.finalState.code.frontend.length + result.finalState.code.backend.length} Files
                </span>
              </div>
              <div className="bg-black p-0 font-mono text-sm max-h-[400px] overflow-y-auto">
                {result.finalState.code.frontend.map((file: any, i: number) => (
                  <div key={i} className="border-b border-gray-800">
                    <div className="p-2 bg-gray-900 text-gray-400 text-xs sticky top-0 border-b border-gray-800 flex gap-2">
                       <Code2 size={14} /> {file.path}
                    </div>
                    <pre className="p-4 text-green-400 overflow-x-auto">
                      <code>{file.content.substring(0, 300)}...</code>
                    </pre>
                  </div>
                ))}
              </div>
            </div>

          </div>
        )}
      </div>
    </main>
  );
}
