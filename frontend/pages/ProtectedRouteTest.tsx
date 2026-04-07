
import React, { useState } from 'react';
import { api } from '../api';

const ProtectedRouteTest = () => {
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const testAdminRoute = async () => {
    setLoading(true);
    setResponse(null);
    setError('');
    try {
      const res = await api.get('/v1/auth/admin-only');
      setResponse(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-900">Protected Route Test</h1>
        <p className="text-gray-500">Test if your current role can access restricted endpoints.</p>
      </header>

      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
        <p className="text-sm text-gray-600 mb-6">
          Click the button below to call <code>GET /v1/auth/admin-only</code>. 
          If you are logged in as a <strong>User</strong>, this should trigger a 403. 
          If you are an <strong>Admin</strong>, you'll see a success message.
        </p>

        <button
          onClick={testAdminRoute}
          disabled={loading}
          className="px-6 py-2 bg-purple-600 text-white rounded-md text-sm font-medium hover:bg-purple-700 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Calling API...' : 'Call Admin-Only Endpoint'}
        </button>

        <div className="mt-8">
          <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">API Result</h3>
          <div className="bg-gray-50 rounded-lg p-4 border border-gray-100 min-h-[100px] flex items-center justify-center">
            {loading && <div className="text-blue-500 animate-pulse">Waiting for server...</div>}
            {!loading && response && (
              <div className="w-full">
                <p className="text-green-600 font-medium">Success!</p>
                <pre className="text-xs mt-2 overflow-auto bg-white p-2 border border-gray-200 rounded">
                  {JSON.stringify(response, null, 2)}
                </pre>
              </div>
            )}
            {!loading && error && (
              <div className="w-full text-center">
                <p className="text-red-500 font-medium">Request Denied</p>
                <p className="text-sm text-gray-600 mt-1">{error}</p>
              </div>
            )}
            {!loading && !response && !error && (
              <p className="text-gray-400 italic">No request made yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProtectedRouteTest;
