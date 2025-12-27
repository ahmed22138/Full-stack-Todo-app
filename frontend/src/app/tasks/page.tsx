/**
 * Modern Tasks Page - Premium Design with Animations
 */
'use client';

import { useState, useEffect } from 'react';
import AuthGuard from '@/components/AuthGuard';
import LogoutButton from '@/components/LogoutButton';
import { useAuth } from '@/hooks/useAuth';
import { tasksAPI } from '@/lib/api';
import type { Task, TaskCreate } from '@/lib/types';

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Create task form state
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [creating, setCreating] = useState(false);

  // Load tasks on mount
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await tasksAPI.getTasks();
      setTasks(data);
    } catch (err: any) {
      setError('Failed to load tasks');
      console.error('Load tasks error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      return;
    }

    try {
      setCreating(true);
      const taskData: TaskCreate = {
        title: newTaskTitle,
        description: newTaskDescription || undefined,
      };

      const newTask = await tasksAPI.createTask(taskData);
      setTasks([newTask, ...tasks]);

      // Reset form
      setNewTaskTitle('');
      setNewTaskDescription('');
      setShowCreateForm(false);
    } catch (err: any) {
      console.error('Create task error:', err);
      alert('Failed to create task');
    } finally {
      setCreating(false);
    }
  };

  const handleToggleComplete = async (taskId: number, currentStatus: boolean) => {
    try {
      const updatedTask = await tasksAPI.toggleTask(taskId, !currentStatus);
      setTasks(tasks.map((t) => (t.id === taskId ? updatedTask : t)));
    } catch (err: any) {
      console.error('Toggle task error:', err);
      alert('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await tasksAPI.deleteTask(taskId);
      setTasks(tasks.filter((t) => t.id !== taskId));
    } catch (err: any) {
      console.error('Delete task error:', err);
      alert('Failed to delete task');
    }
  };

  const stats = {
    total: tasks.length,
    active: tasks.filter((t) => !t.completed).length,
    completed: tasks.filter((t) => t.completed).length,
  };

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        {/* Modern Header */}
        <header className="bg-white/70 backdrop-blur-lg border-b border-gray-200/50 sticky top-0 z-10 shadow-sm">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                    TaskFlow
                  </h1>
                  <p className="text-xs sm:text-sm text-gray-600">{user?.email}</p>
                </div>
              </div>
              <LogoutButton />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Stats Cards */}
          <div className="grid grid-cols-3 gap-3 sm:gap-4 mb-8">
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-4 sm:p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs sm:text-sm text-gray-600 font-medium">Total</p>
                  <p className="text-2xl sm:text-3xl font-bold text-gray-900 mt-1">{stats.total}</p>
                </div>
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
                  <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-4 sm:p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs sm:text-sm text-gray-600 font-medium">Active</p>
                  <p className="text-2xl sm:text-3xl font-bold text-orange-600 mt-1">{stats.active}</p>
                </div>
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl flex items-center justify-center">
                  <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-4 sm:p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs sm:text-sm text-gray-600 font-medium">Done</p>
                  <p className="text-2xl sm:text-3xl font-bold text-green-600 mt-1">{stats.completed}</p>
                </div>
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center">
                  <svg className="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Create Task Button/Form */}
          {!showCreateForm ? (
            <button
              onClick={() => setShowCreateForm(true)}
              className="w-full mb-6 px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-2xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 shadow-lg transform transition-all duration-200 hover:scale-[1.02] flex items-center justify-center space-x-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              <span>Create New Task</span>
            </button>
          ) : (
            <div className="mb-6 p-6 bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-gray-100">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Create New Task</h2>
                <button
                  onClick={() => {
                    setShowCreateForm(false);
                    setNewTaskTitle('');
                    setNewTaskDescription('');
                  }}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <form onSubmit={handleCreateTask} className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                    Title *
                  </label>
                  <input
                    type="text"
                    id="title"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    required
                    maxLength={200}
                    className="block w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200"
                    placeholder="What needs to be done?"
                  />
                </div>
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                    Description
                  </label>
                  <textarea
                    id="description"
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    maxLength={2000}
                    rows={3}
                    className="block w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 resize-none"
                    placeholder="Add more details... (optional)"
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    type="submit"
                    disabled={creating}
                    className="flex-1 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium rounded-xl hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50 shadow-lg transform transition-all duration-200 hover:scale-[1.02]"
                  >
                    {creating ? 'Creating...' : 'Create Task'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-center space-x-2">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span>{error}</span>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="text-center py-20">
              <div className="inline-block">
                <div className="w-16 h-16 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
              </div>
              <p className="mt-4 text-gray-600 font-medium">Loading your tasks...</p>
            </div>
          )}

          {/* Empty State */}
          {!loading && tasks.length === 0 && (
            <div className="text-center py-20 bg-white/50 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-100">
              <div className="w-20 h-20 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-10 h-10 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <p className="text-gray-600 text-lg font-medium">No tasks yet</p>
              <p className="text-gray-400 mt-2">Create your first task to get started!</p>
            </div>
          )}

          {/* Task List */}
          {!loading && tasks.length > 0 && (
            <div className="space-y-3">
              {tasks.map((task, index) => (
                <div
                  key={task.id}
                  className="group p-5 bg-white/80 backdrop-blur-sm rounded-2xl shadow-md hover:shadow-xl border border-gray-100 transition-all duration-300 hover:scale-[1.01] animate-fade-in"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <div className="flex items-start gap-4">
                    {/* Checkbox */}
                    <div className="flex-shrink-0 pt-1">
                      <button
                        onClick={() => handleToggleComplete(task.id, task.completed)}
                        className="w-6 h-6 rounded-lg border-2 border-gray-300 flex items-center justify-center hover:border-indigo-600 transition-all duration-200"
                        style={{
                          backgroundColor: task.completed ? '#6366f1' : 'transparent',
                          borderColor: task.completed ? '#6366f1' : undefined,
                        }}
                      >
                        {task.completed && (
                          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </button>
                    </div>

                    {/* Task Content */}
                    <div className="flex-1 min-w-0">
                      <h3
                        className={`text-base sm:text-lg font-semibold transition-all duration-200 ${
                          task.completed
                            ? 'line-through text-gray-400'
                            : 'text-gray-900 group-hover:text-indigo-600'
                        }`}
                      >
                        {task.title}
                      </h3>
                      {task.description && (
                        <p
                          className={`mt-1 text-sm transition-all duration-200 ${
                            task.completed ? 'text-gray-400' : 'text-gray-600'
                          }`}
                        >
                          {task.description}
                        </p>
                      )}
                      <div className="flex items-center mt-3 space-x-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          task.completed
                            ? 'bg-green-100 text-green-800'
                            : 'bg-orange-100 text-orange-800'
                        }`}>
                          {task.completed ? 'Completed' : 'Active'}
                        </span>
                        <span className="text-xs text-gray-400">
                          {new Date(task.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>

                    {/* Delete Button */}
                    <button
                      onClick={() => handleDeleteTask(task.id)}
                      className="flex-shrink-0 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200 opacity-0 group-hover:opacity-100"
                      title="Delete task"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </AuthGuard>
  );
}
