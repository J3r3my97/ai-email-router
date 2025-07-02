import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { tempEmailAPI, dashboardAPI } from '@/lib/api';
import { format } from 'date-fns';

interface DashboardProps {
  isAuthenticated: boolean;
  setIsAuthenticated: (value: boolean) => void;
}

interface TempEmail {
  id: number;
  address: string;
  purpose: string;
  expires_at: string;
  is_active: boolean;
  created_at: string;
}

interface EmailLog {
  id: number;
  sender_email: string;
  subject: string;
  action_taken: string;
  ai_confidence_score: number;
  created_at: string;
}

interface Stats {
  total_temp_emails: number;
  active_temp_emails: number;
  emails_forwarded: number;
  emails_deleted: number;
  recent_activity: EmailLog[];
}

export default function Dashboard({ isAuthenticated, setIsAuthenticated }: DashboardProps) {
  const [tempEmails, setTempEmails] = useState<TempEmail[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [newEmailPurpose, setNewEmailPurpose] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    fetchData();
  }, [isAuthenticated, router]);

  const fetchData = async () => {
    try {
      const [tempEmailsRes, statsRes] = await Promise.all([
        tempEmailAPI.list(),
        dashboardAPI.stats(),
      ]);
      setTempEmails(tempEmailsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTempEmail = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await tempEmailAPI.create(newEmailPurpose);
      setNewEmailPurpose('');
      setShowCreateForm(false);
      fetchData();
    } catch (error) {
      console.error('Error creating temp email:', error);
    }
  };

  const handleDeactivate = async (id: number) => {
    if (confirm('Are you sure you want to deactivate this email address?')) {
      try {
        await tempEmailAPI.deactivate(id);
        fetchData();
      } catch (error) {
        console.error('Error deactivating email:', error);
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    router.push('/');
  };

  if (!isAuthenticated) {
    return null;
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">AI Email Router</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Total Emails</dt>
                      <dd className="text-lg font-medium text-gray-900">{stats.total_temp_emails}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-green-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Active</dt>
                      <dd className="text-lg font-medium text-gray-900">{stats.active_temp_emails}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Forwarded</dt>
                      <dd className="text-lg font-medium text-gray-900">{stats.emails_forwarded}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-red-100 rounded-md flex items-center justify-center">
                      <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Deleted</dt>
                      <dd className="text-lg font-medium text-gray-900">{stats.emails_deleted}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Temporary Email Addresses
                </h3>
                <button
                  onClick={() => setShowCreateForm(true)}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                >
                  Create New
                </button>
              </div>

              {showCreateForm && (
                <form onSubmit={handleCreateTempEmail} className="mb-6 p-4 bg-gray-50 rounded-md">
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Purpose (optional)
                    </label>
                    <input
                      type="text"
                      value={newEmailPurpose}
                      onChange={(e) => setNewEmailPurpose(e.target.value)}
                      placeholder="e.g., Netflix trial, Concert tickets"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      type="submit"
                      className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                    >
                      Create
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowCreateForm(false)}
                      className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-400"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              )}

              <div className="space-y-3">
                {tempEmails.map((email) => (
                  <div key={email.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">{email.address}</p>
                      {email.purpose && (
                        <p className="text-sm text-gray-500">{email.purpose}</p>
                      )}
                      <p className="text-xs text-gray-400">
                        Created {format(new Date(email.created_at), 'MMM d, yyyy')}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        email.is_active 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {email.is_active ? 'Active' : 'Inactive'}
                      </span>
                      {email.is_active && (
                        <button
                          onClick={() => handleDeactivate(email.id)}
                          className="text-red-600 hover:text-red-800 text-sm"
                        >
                          Deactivate
                        </button>
                      )}
                    </div>
                  </div>
                ))}
                {tempEmails.length === 0 && (
                  <p className="text-gray-500 text-center py-4">No temporary emails created yet.</p>
                )}
              </div>
            </div>
          </div>

          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Recent Activity
              </h3>
              <div className="space-y-3">
                {stats?.recent_activity.map((log) => (
                  <div key={log.id} className="border-l-4 border-gray-200 pl-4">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-gray-900">{log.subject}</p>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        log.action_taken === 'forward' 
                          ? 'bg-blue-100 text-blue-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {log.action_taken}
                      </span>
                    </div>
                    <p className="text-sm text-gray-500">From: {log.sender_email}</p>
                    <p className="text-xs text-gray-400">
                      {format(new Date(log.created_at), 'MMM d, h:mm a')}
                    </p>
                  </div>
                ))}
                {(!stats?.recent_activity || stats.recent_activity.length === 0) && (
                  <p className="text-gray-500 text-center py-4">No recent activity.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}