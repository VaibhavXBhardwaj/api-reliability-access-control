import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const RateLimitTest = () => {
  const [results, setResults] = useState<{ status: number; message: string; timestamp: string }[]>([]);
  const [isTesting, setIsTesting] = useState(false);

  const spamLogin = async () => {
    setIsTesting(true);
    setResults([]);
    
    // Fire 10 rapid requests with bad credentials
    const requests = Array.from({ length: 10 }).map(async () => {
      try {
        const response = await axios.post(`${API_BASE}/v1/auth/login`, {
          email: 'nonexistent@test.com',
          password: 'wrongpassword'
        });
        return { status: response.status, message: 'Success (Unexpected)', timestamp: new Date().toLocaleTimeString() };
      } catch (err: any) {
        return { 
          status: err.response?.status || 0, 
          message: err.response?.status === 429 ? 'Rate Limited' : 'Unauthorized',
          timestamp: new Date().toLocaleTimeString()
        };
      }
    });

    const outcomes = await Promise.all(requests);
    setResults(outcomes);
    setIsTesting(false);
  };

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-900">Rate Limit Test</h1>
        <p className="text-gray-500">Simulate a brute-force attack to test API throttling.</p>
      </header>

      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
        <p className="text-sm text-gray-600 mb-6">
          Pressing the button below will trigger 10 simultaneous login attempts with invalid credentials. 
          If the backend is configured with rate limiting, some requests should return <code>429 Too Many Requests</code>.
        </p>

        <button
          onClick={spamLogin}
          disabled={isTesting}
          className="px-6 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700 disabled:opacity-50 transition-colors shadow-sm"
        >
          {isTesting ? 'Spamming API...' : 'Spam Login API'}
        </button>

        <div className="mt-8">
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Results Batch</h3>
          <div className="overflow-hidden border border-gray-200 rounded-lg">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status Code</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Server Message</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {results.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="px-6 py-8 text-center text-sm text-gray-400 italic">
                      {isTesting ? 'Executing requests...' : 'No test results yet.'}
                    </td>
                  </tr>
                ) : (
                  results.map((res, idx) => (
                    <tr key={idx}>
                      <td className="px-6 py-4 whitespace-nowrap text-xs text-gray-500">{res.timestamp}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-mono font-bold">
                        <span className={`px-2 py-1 rounded ${
                          res.status === 429 ? 'bg-red-100 text-red-700' : 
                          res.status === 401 ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'
                        }`}>
                          {res.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{res.message}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RateLimitTest;
