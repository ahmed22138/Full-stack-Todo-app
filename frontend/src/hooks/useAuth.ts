/**
 * Authentication hook for managing user auth state
 */
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI } from '@/lib/api';
import type { User, RegisterRequest, LoginRequest } from '@/lib/types';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = () => {
      try {
        const storedUser = localStorage.getItem('user');
        const token = localStorage.getItem('access_token');

        if (storedUser && token) {
          setUser(JSON.parse(storedUser));
        }
      } catch (err) {
        console.error('Failed to load user from localStorage:', err);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  /**
   * Register a new user
   */
  const register = async (data: RegisterRequest) => {
    try {
      setError(null);
      setLoading(true);

      // Register user
      const newUser = await authAPI.register(data);

      // Auto-login after registration
      const authResponse = await authAPI.login({
        email: data.email,
        password: data.password,
      });

      setUser(authResponse.user);
      router.push('/tasks');
    } catch (err: any) {
      const errorMsg =
        err.response?.data?.error ||
        err.response?.data?.message ||
        'Registration failed';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Login with email and password
   */
  const login = async (credentials: LoginRequest) => {
    try {
      setError(null);
      setLoading(true);

      const authResponse = await authAPI.login(credentials);
      setUser(authResponse.user);
      router.push('/tasks');
    } catch (err: any) {
      const errorMsg =
        err.response?.data?.error ||
        err.response?.data?.message ||
        'Login failed';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout current user
   */
  const logout = async () => {
    try {
      setLoading(true);
      await authAPI.logout();
      setUser(null);
      router.push('/login');
    } catch (err: any) {
      console.error('Logout error:', err);
      // Clear state even if API call fails
      setUser(null);
      router.push('/login');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Refresh user data from server
   */
  const refreshUser = async () => {
    try {
      const currentUser = await authAPI.getCurrentUser();
      setUser(currentUser);
      localStorage.setItem('user', JSON.stringify(currentUser));
    } catch (err) {
      console.error('Failed to refresh user:', err);
      // If refresh fails, logout user
      await logout();
    }
  };

  return {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    register,
    login,
    logout,
    refreshUser,
  };
}
