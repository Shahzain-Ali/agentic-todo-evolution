'use client';

import { useState, FormEvent } from 'react';
import { authenticatedRequest } from '@/lib/api-client';
import type { TaskCreate } from '@/lib/definitions';

interface AddTaskFormProps {
  onTaskAdded: () => void;
}

export default function AddTaskForm({ onTaskAdded }: AddTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const validateForm = (): boolean => {
    if (!title.trim()) {
      setError('Title is required');
      return false;
    }

    if (title.length > 200) {
      setError('Title must be 200 characters or less');
      return false;
    }

    if (description.length > 2000) {
      setError('Description must be 2000 characters or less');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const taskData: TaskCreate = {
        title: title.trim(),
        description: description.trim() || undefined,
      };

      // authenticatedRequest now automatically gets JWT token from Better Auth
      await authenticatedRequest('/api/tasks', {
        method: 'POST',
        body: JSON.stringify(taskData),
      });

      // Clear form
      setTitle('');
      setDescription('');

      // Notify parent to refresh task list
      onTaskAdded();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-gray-200/50 shadow-sm p-6 mb-8 transition-all duration-300 hover:shadow-lg hover:border-blue-200">
      {error && (
        <div className="mb-4 bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded-r text-sm animate-in fade-in slide-in-from-top-2 duration-300">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 mt-1">
              <div className="w-5 h-5 rounded-full border-2 border-gray-300 group-hover:border-blue-400 transition-colors"></div>
            </div>
            <div className="flex-1 space-y-3">
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-0 py-2 text-base font-medium text-gray-900 border-0 focus:ring-0 focus:outline-none placeholder:text-gray-400 bg-transparent"
                placeholder="What needs to be done?"
                required
                maxLength={200}
                disabled={loading}
                autoComplete="off"
              />

              {(title.length > 0 || description.length > 0) && (
                <textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-0 py-2 text-sm text-gray-600 border-0 focus:ring-0 focus:outline-none resize-none placeholder:text-gray-400 bg-transparent animate-in fade-in slide-in-from-top-2 duration-200"
                  placeholder="Add more details..."
                  rows={2}
                  maxLength={2000}
                  disabled={loading}
                />
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between pt-3 border-t border-gray-100">
          <div className="flex items-center gap-3 text-xs text-gray-400">
            {title.length > 0 && (
              <span className="px-2 py-1 bg-gray-100 rounded-lg transition-all duration-200">
                {title.length}/200
              </span>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || !title.trim()}
            className="group px-6 py-2.5 bg-gradient-to-r from-blue-500 to-blue-600 text-white text-sm font-semibold rounded-xl hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 hover:scale-105"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Adding...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                Add Task
                <svg className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                </svg>
              </span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
