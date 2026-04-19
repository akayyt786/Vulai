"use client";

import React, { useState, useEffect } from 'react';
import { AlertTriangle, Filter, LayoutGrid, Loader2 } from 'lucide-react';
import { clsx } from 'clsx';
import { api, Finding } from '@/lib/api';

export const FindingsMatrix = ({ scanId }: { scanId: string }) => {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!scanId) return;

    const fetchFindings = async () => {
      setIsLoading(true);
      try {
        const data = await api.getFindings(scanId);
        setFindings(data);
      } catch (err) {
        console.error("Failed to fetch findings:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchFindings();
    
    // Poll for new findings every 10 seconds while scan is active
    const interval = setInterval(fetchFindings, 10000);
    return () => clearInterval(interval);
  }, [scanId]);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-danger border-danger/20 bg-danger/5';
      case 'high': return 'text-orange-500 border-orange-500/20 bg-orange-500/5';
      case 'medium': return 'text-yellow-500 border-yellow-500/20 bg-yellow-500/5';
      case 'low': return 'text-blue-500 border-blue-500/20 bg-blue-500/5';
      default: return 'text-secondary border-secondary/20 bg-secondary/5';
    }
  };

  return (
    <div className="tech-card p-6 flex flex-col h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <LayoutGrid size={18} className="text-secondary" />
          <h2 className="text-sm font-semibold uppercase tracking-wider">Attack Surface Findings</h2>
        </div>
        <div className="flex items-center gap-4">
          {isLoading && <Loader2 size={12} className="animate-spin text-secondary" />}
          <button className="text-[10px] flex items-center gap-1 text-secondary hover:text-primary transition-colors">
            <Filter size={12} />
            <span>FILTER RESULTS</span>
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar">
        {!scanId ? (
          <div className="h-full flex flex-col items-center justify-center text-secondary opacity-30 space-y-2">
            <LayoutGrid size={48} />
            <p className="text-[10px] tracking-widest uppercase">Select or start a scan to view results</p>
          </div>
        ) : findings.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-secondary opacity-50 space-y-2">
            <AlertTriangle size={32} />
            <p className="text-[10px] tracking-widest uppercase">{isLoading ? "FETCHING..." : "No findings reported yet"}</p>
          </div>
        ) : (
          <table className="w-full text-left text-xs">
            <thead className="text-secondary border-b border-border">
              <tr>
                <th className="pb-2 font-medium">SEVERITY</th>
                <th className="pb-2 font-medium">DESCRIPTION</th>
                <th className="pb-2 font-medium">SURFACE</th>
                <th className="pb-2 font-medium">LOCATION</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50">
              {findings.map((f) => (
                <tr key={f.id} className="hover:bg-white/[0.02] transition-colors group">
                  <td className="py-3 pr-4">
                    <span className={clsx(
                      "px-2 py-0.5 rounded-full border text-[9px] font-bold uppercase",
                      getSeverityColor(f.severity)
                    )}>
                      {f.severity}
                    </span>
                  </td>
                  <td className="py-3 pr-4 font-medium text-primary group-hover:text-white transition-colors">{f.title}</td>
                  <td className="py-3 pr-4 text-secondary uppercase tracking-tighter text-[10px]">{f.surface}</td>
                  <td className="py-3 text-secondary font-mono truncate max-w-[150px]">{f.location}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};
