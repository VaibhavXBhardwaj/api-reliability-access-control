
import React, { useState } from 'react';
import { api } from '../api';

const AdminPage = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchAdminData = async () => {
    setLoading(true);
    try {
      const response = await api.get('/v1/auth/admin-only');
      setData(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-900">Admin Panel (RBAC)</h1>
        <p className="text-gray-500">This view is only accessible to users with <code>role === "admin"</code>.</p>
      </header>

      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm border-l-4 border-l-purple-500">
        <h2 className="text-lg font-bold text-gray-800 mb-2">Restricted Area</h2>
        <p className="text-sm text-gray-600 mb-4">
          You are seeing this because your decoded JWT includes the admin role. 
          Use this section to manage system-wide settings or view sensitive data.
        </p>

        <button
          onClick={fetchAdminData}
          disabled={loading}
          className="px-4 py-2 bg-gray-800 text-white rounded-md text-sm font-medium hover:bg-gray-900 transition-colors"
        >
          {loading ? 'Fetching...' : 'Fetch Admin Secret'}
        </button>

        {data && (
          <div className="mt-4 p-4 bg-purple-50 rounded-md border border-purple-100 text-sm">
            <span className="font-bold text-purple-700">Server Response:</span>
            <span className="ml-2 text-purple-900">{data.message || 'Access Granted'}</span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="bg-white p-4 rounded-lg border border-gray-100 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-xs text-gray-400 font-semibold uppercase">Metric {i}</p>
              <p className="text-xl font-bold text-gray-800">{(Math.random() * 100).toFixed(1)}%</p>
            </div>
            <div className="text-2xl">📈</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminPage;
