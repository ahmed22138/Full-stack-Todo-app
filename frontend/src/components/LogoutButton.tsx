/**
 * Modern Logout button component
 */
'use client';

import { useAuth } from '@/hooks/useAuth';

export default function LogoutButton() {
  const { logout, loading } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  return (
    <button
      onClick={handleLogout}
      disabled={loading}
      className="group flex items-center space-x-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white/50 hover:bg-red-50 border border-gray-200 hover:border-red-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:scale-105 shadow-sm hover:shadow-md"
    >
      {loading ? (
        <>
          <svg className="animate-spin h-4 w-4 text-gray-600" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="hidden sm:inline">Logging out...</span>
        </>
      ) : (
        <>
          <svg className="w-4 h-4 text-gray-600 group-hover:text-red-600 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span className="hidden sm:inline group-hover:text-red-600 transition-colors duration-200">Logout</span>
        </>
      )}
    </button>
  );
}
