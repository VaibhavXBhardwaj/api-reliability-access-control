
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user, refresh } = useAuth();
  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    if (!user) return;

    const calculateTimeLeft = () => {
      const now = Math.floor(Date.now() / 1000);
      const difference = user.exp - now;
      setTimeLeft(difference > 0 ? difference : 0);
    };

    calculateTimeLeft();
    const timer = setInterval(calculateTimeLeft, 1000);

    return () => clearInterval(timer);
  }, [user]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await refresh();
    } catch (err) {
      console.error('Manual refresh failed', err);
    } finally {
      setIsRefreshing(false);
    }
  };

  const formatTime = (seconds: number) => {
    if (seconds === null) return '--:--';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-gray-900">User Dashboard</h1>
        <p className="text-gray-500">Authenticated session details and token management.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* User Card */}
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">User Profile</h2>
          <div className="space-y-3">
            <div>
              <p className="text-xs text-gray-500">User ID</p>
              <p className="font-mono text-sm">{user?.id}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Email</p>
              <p className="text-sm font-medium">{user?.email}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Current Role</p>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                user?.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
              }`}>
                {user?.role}
              </span>
            </div>
          </div>
        </div>

        {/* Token Card */}
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Token Expiry</h2>
          <div className="flex flex-col items-center justify-center space-y-4 py-2">
            <div className={`text-4xl font-mono font-bold ${timeLeft && timeLeft < 60 ? 'text-red-500' : 'text-gray-800'}`}>
              {timeLeft !== null ? formatTime(timeLeft) : '00:00'}
            </div>
            <p className="text-xs text-gray-500 text-center">
              Access token expires soon. The interceptor will auto-refresh on 401.
            </p>
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              {isRefreshing ? 'Refreshing...' : 'Manual Token Refresh'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
