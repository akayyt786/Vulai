const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Scan {
  id: string;
  status: 'pending' | 'running' | 'done' | 'failed';
  input_type: string;
  input_value: string;
  current_layer: number;
  surfaces_covered: string[];
  created_at: string;
}

export interface Finding {
  id: string;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  location: string;
  evidence: string;
  surface: string;
  layer: number;
}

export interface ScanStep {
  step_number: number;
  tool_name: string;
  ai_reasoning: string;
  findings_count: number;
  duration_ms: number;
  created_at: string;
}

export const api = {
  createScan: async (target: string, inputType: string = 'url') => {
    const response = await fetch(`${API_BASE_URL}/api/scans/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        input_type: inputType,
        input_value: target,
        consent_confirmed: true
      })
    });
    if (!response.ok) throw new Error('Failed to create scan');
    return response.json();
  },

  getScan: async (scanId: string) => {
    const response = await fetch(`${API_BASE_URL}/api/scans/${scanId}/`);
    if (!response.ok) throw new Error('Failed to fetch scan');
    return response.json();
  },

  getFindings: async (scanId: string) => {
    const response = await fetch(`${API_BASE_URL}/api/scans/${scanId}/`);
    if (!response.ok) throw new Error('Failed to fetch findings');
    const data = await response.json();
    return data.findings || [];
  },

  getReport: async (scanId: string) => {
    const response = await fetch(`${API_BASE_URL}/api/scans/${scanId}/report/`);
    if (!response.ok) throw new Error('Report not ready');
    return response.json();
  }
};
