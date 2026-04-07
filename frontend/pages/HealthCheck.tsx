import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const HealthCheck = () => {
  const [status, setStatus] = useState<'loading' | 'up' | 'down'>('loading');
  const [lastCheck, setLastCheck] = useState<string>('');

  const checkHealth = async () => {
    setStatus('loading');
    try {
      // Use deployed backend URL from environment variable
      const response = await axios.get(`${API_BASE}/health`);
      if (response.status === 200) {
        setStatus('up');
      } else {
        setStatus('down');
      }
    } catch (err) {
      setStatus('down');
    } finally {
      setLastCheck(new Date().toLocaleTimeString());
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-900">Service Health</h1>
        <p className="text-gray-500">Monitor the live status of the FastAPI backend.</p>
      </header>

      <div className="bg-white p-8 rounded-lg border border-gray-200 shadow-sm flex flex-col items-center justify-center text-center">
        <div className={`w-20 h-20 rounded-full flex items-center justify-center text-4xl mb-4 ${
          status === 'up' ? 'bg-green-100' : status === 'down' ? 'bg-red-100' : 'bg-blue-100'
        }`}>
          {status === 'up' ? '✅' : status === 'down' ? '❌' : '⏳'}
        </div>
        
        <h2 className={`text-xl font-bold ${
          status === 'up' ? 'text-green-700' : status === 'down' ? 'text-red-700' : 'text-blue-700'
        }`}>
          {status === 'up' ? 'API is Healthy' : status === 'down' ? 'API is Down' : 'Checking...'}
        </h2>
        
        <p className="text-sm text-gray-500 mt-2">
          Checked target: <code>{`${API_BASE}/health`}</code>
        </p>
        
        <div className="mt-8 pt-8 border-t border-gray-100 w-full">
          <p className="text-xs text-gray-400 font-medium uppercase tracking-widest mb-4">Last Verification</p>
          <p className="text-sm font-mono font-bold text-gray-800">{lastCheck || 'In progress...'}</p>
          <button
            onClick={checkHealth}
            className="mt-4 px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
          >
            Refresh Status
          </button>
        </div>
      </div>
    </div>
  );
};

export default HealthCheck;
