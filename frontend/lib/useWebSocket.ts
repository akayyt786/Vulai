import { useState, useEffect, useRef, useCallback } from 'react';

export const useWebSocket = (url: string | null) => {
  const [data, setData] = useState<any>(null);
  const [status, setStatus] = useState<'connecting' | 'open' | 'closed'>('closed');
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    if (!url) return;

    setStatus('connecting');
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log('WS Connected:', url);
      setStatus('open');
    };

    socket.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      } catch (err) {
        console.error('WS Message Parse Error:', err);
      }
    };

    socket.onclose = () => {
      setStatus('closed');
      // Auto-reconnect after 3 seconds
      reconnectTimeoutRef.current = setTimeout(() => {
        console.log('WS Reconnecting...');
        connect();
      }, 3000);
    };

    socket.onerror = (err) => {
      console.error('WS Error:', err);
      socket.close();
    };
  }, [url]);

  useEffect(() => {
    connect();
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connect]);

  const sendMessage = useCallback((msg: any) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(msg));
    }
  }, []);

  return { data, status, sendMessage };
};
