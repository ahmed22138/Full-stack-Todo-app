/**
 * AuthGuard component - protects routes from unauthenticated access
 */
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean; // If true, user must be authenticated
}

export default function AuthGuard({
  children,
  requireAuth = true,
}: AuthGuardProps) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return; // Wait for auth check to complete

    if (requireAuth && !isAuthenticated) {
      // User must be authenticated but isn't - redirect to login
      router.push('/login');
    } else if (!requireAuth && isAuthenticated) {
      // User shouldn't be authenticated (e.g., on login page) but is - redirect to tasks
      router.push('/tasks');
    }
  }, [isAuthenticated, loading, requireAuth, router]);

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render protected content until auth check is complete
  if (requireAuth && !isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  if (!requireAuth && isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  return <>{children}</>;
}
