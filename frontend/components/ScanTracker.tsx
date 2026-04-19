"use client";

import React, { useState, useEffect } from 'react';
import { Terminal, Shield, Activity, ChevronRight, Wifi, WifiOff } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useWebSocket } from '@/lib/useWebSocket';

interface Step {
  id: string;
  tool: string;
  reasoning: string;
  status: 'running' | 'done' | 'failed';
  timestamp: string;
}

export const ScanTracker = ({ scanId }: { scanId: string }) => {
  const [steps, setSteps] = useState<Step[]>([]);
  const [statusText, setStatusText] = useState("AWAITING COMMAND INITIALIZATION...");
  
  const wsUrl = scanId ? `ws://${window.location.host}/ws/scans/${scanId}/` : null;
  const { data, status } = useWebSocket(wsUrl);

  useEffect(() => {
    if (data?.type === 'update') {
      const message = data.data;
      if (message.type === 'status') {
        setStatusText(message.text);
      } else if (message.type === 'step') {
        setSteps(prev => [...prev, {
          id: message.id || Math.random().toString(),
          tool: message.tool,
          reasoning: message.reasoning,
          status: message.status || 'done',
          timestamp: new Date().toLocaleTimeString()
        }]);
      } else if (message.type === 'scan_complete') {
        setStatusText("SCAN COMPLETED");
      }
    }
  }, [data]);

  // Reset steps when scanId changes
  useEffect(() => {
    if (scanId) {
      setSteps([]);
      setStatusText("INITIALIZING ENGINE...");
    }
  }, [scanId]);

  return (
    <div className="tech-card p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Terminal size={18} className="text-accent" />
          <h2 className="text-sm font-semibold uppercase tracking-wider">Live Execution Engine</h2>
        </div>
        <div className="flex items-center gap-2 text-[10px] text-secondary">
          {status === 'open' ? (
            <Activity size={12} className="animate-pulse text-success" />
          ) : (
            <WifiOff size={12} className="text-error" />
          )}
          <span className={status === 'open' ? "text-success" : "text-error"}>
            {status === 'open' ? "AUTONOMOUS ORCHESTRATOR ONLINE" : "ENGINE DISCONNECTED"}
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 font-mono text-xs pr-2 custom-scrollbar">
        <AnimatePresence>
          {steps.map((step, idx) => (
            <motion.div 
              key={step.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="border-l-2 border-border pl-4 py-1"
            >
              <div className="text-secondary mb-1">[{step.timestamp}] STEP_{idx + 1}</div>
              <div className="flex items-start gap-2">
                <ChevronRight size={14} className="mt-0.5 text-accent" />
                <div>
                  <span className="text-primary font-bold">{step.tool}</span>
                  <p className="text-secondary mt-1 italic">{step.reasoning}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {steps.length === 0 && (
          <div className="text-secondary flex flex-col items-center justify-center h-full opacity-50 text-center">
            <Shield size={48} className="mb-4 text-border" />
            <p className="uppercase tracking-widest text-[10px]">{statusText}</p>
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-border flex items-center gap-4 text-[10px] text-secondary">
        <div className="flex-1 truncate">ID: <span className="text-primary">{scanId || "NONE"}</span></div>
        <div className="flex items-center gap-1">
          {status === 'open' ? <Wifi size={10} className="text-success" /> : <WifiOff size={10} />}
          <span className="uppercase">{status}</span>
        </div>
      </div>
    </div>
  );
};
