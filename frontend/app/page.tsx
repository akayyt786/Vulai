"use client";

import React, { useState } from 'react';
import { ScanTracker } from '@/components/ScanTracker';
import { FindingsMatrix } from '@/components/FindingsMatrix';
import { api } from '@/lib/api';
import { Shield, Target, Plus, Search, HelpCircle, User, Loader2 } from 'lucide-react';

export default function Dashboard() {
  const [activeScanId, setActiveScanId] = useState<string>("");
  const [target, setTarget] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const handleStartScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!target) return;
    
    setIsLoading(true);
    try {
      const result = await api.createScan(target);
      setActiveScanId(result.scan_id);
    } catch (err) {
      console.error("Failed to start scan:", err);
      alert("Error initializing scan. Is the backend running?");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen bg-background text-foreground selection:bg-accent/30">
      {/* Sidebar - Simple & Techie */}
      <aside className="w-16 border-r border-border flex flex-col items-center py-8 gap-10">
        <div className="w-10 h-10 bg-accent rounded flex items-center justify-center">
          <Shield size={24} className="text-white" />
        </div>
        <nav className="flex-1 flex flex-col gap-8 text-secondary">
          <Search size={20} className="hover:text-primary cursor-pointer transition-colors" />
          <Target size={20} className="text-primary cursor-pointer border-r-2 border-primary pr-1 ml-1" />
          <HelpCircle size={20} className="hover:text-primary cursor-pointer transition-colors" />
        </nav>
        <div className="w-8 h-8 rounded-full bg-border flex items-center justify-center text-secondary border border-border">
          <User size={16} />
        </div>
      </aside>

      {/* Main Content Area */}
      <section className="flex-1 flex flex-col p-8 gap-8 overflow-hidden">
        {/* Header Section */}
        <header className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">VulnAI Orchestrator</h1>
            <p className="text-secondary text-xs mt-1 uppercase tracking-widest opacity-60">Phase 2 // Autonomous Security Discovery</p>
          </div>
          
          <form onSubmit={handleStartScan} className="flex gap-2">
            <div className="relative">
              <input 
                type="text" 
                placeholder="ENTER TARGET DOMAIN OR IP..."
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                className="bg-black border border-border px-4 py-2 rounded text-xs w-[300px] focus:outline-none focus:border-accent transition-colors font-mono"
                disabled={isLoading}
              />
            </div>
            <button 
              type="submit"
              disabled={isLoading || !target}
              className="bg-primary text-black px-4 py-2 rounded text-[10px] font-bold uppercase hover:bg-white/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              {isLoading ? <Loader2 size={14} className="animate-spin" /> : <Plus size={14} />}
              {isLoading ? "Initializing..." : "Initialize Scan"}
            </button>
          </form>
        </header>

        {/* Dashboard Grid */}
        <div className="flex-1 grid grid-cols-12 gap-6 min-h-0">
          {/* Left Panel: Live Engine */}
          <div className="col-span-5 flex flex-col min-h-0">
            <ScanTracker scanId={activeScanId} />
          </div>

          {/* Right Panel: Findings & Stats */}
          <div className="col-span-7 flex flex-col gap-6 min-h-0 overflow-y-auto">
            <div className="flex-1">
              <FindingsMatrix scanId={activeScanId} />
            </div>
            
            {/* Quick Stats / Chain Preview */}
            <div className="h-[180px] tech-card p-6 flex flex-col">
              <div className="flex items-center gap-2 text-secondary mb-4">
                <Target size={16} />
                <h3 className="text-[10px] font-bold uppercase tracking-widest">Attack Chain Intelligence</h3>
              </div>
              <div className="flex-1 flex items-center justify-center border-2 border-dashed border-border rounded opacity-30 text-[9px] tracking-[0.2em] font-mono whitespace-pre text-center">
                {activeScanId ? "ANALYSING SCAN DATA FOR CHAINS..." : "AWAITING SUFFICIENT FINDINGS FOR CHAIN ANALYSIS"}
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
