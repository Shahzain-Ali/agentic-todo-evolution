'use client';

import { useState } from 'react';
import { authenticatedRequest } from '@/lib/api-client';
import type { Task, TaskUpdate } from '@/lib/definitions';

interface TaskCardProps {
  task: Task;
  onUpdate: () => void;
}

export default function TaskCard({ task, onUpdate }: TaskCardProps) {
  const [isCompleted, setIsCompleted] = useState(task.status === 'completed');
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleToggleStatus = async () => {
    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Not authenticated');
        return;
      }

      const newStatus = isCompleted ? 'pending' : 'completed';
      const updateData: TaskUpdate = { status: newStatus };

      await authenticatedRequest(`/api/tasks/${task.id}`, token, {
        method: 'PUT',
        body: JSON.stringify(updateData),
      });

      setIsCompleted(!isCompleted);
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Not authenticated');
        return;
      }

      const updateData: TaskUpdate = {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      };

      await authenticatedRequest(`/api/tasks/${task.id}`, token, {
        method: 'PUT',
        body: JSON.stringify(updateData),
      });

      setIsEditing(false);
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
    setError('');
  };

  const handleDelete = async () => {
    // Confirmation dialog
    const confirmed = window.confirm(
      `Are you sure you want to delete "${task.title}"? This action cannot be undone.`
    );

    if (!confirmed) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Not authenticated');
        return;
      }

      await authenticatedRequest(`/api/tasks/${task.id}`, token, {
        method: 'DELETE',
      });

      // Notify parent to refresh task list
      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      setLoading(false);
    }
  };

  if (isEditing) {
    return (
      <div className="group bg-white rounded-xl border border-gray-200 p-5 transition-all duration-200 hover:shadow-md animate-in fade-in slide-in-from-top-2 duration-300">
        {error && (
          <div className="mb-4 bg-red-50 border-l-4 border-red-400 text-red-700 px-4 py-3 rounded-r text-sm animate-in fade-in slide-in-from-top-1 duration-200">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              placeholder="Task title"
              className="w-full px-0 py-2 text-lg font-medium border-0 border-b-2 border-gray-200 focus:border-primary focus:ring-0 focus:outline-none transition-colors placeholder:text-gray-400"
              maxLength={200}
              disabled={loading}
              autoFocus
            />
          </div>

          <div>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              placeholder="Add description..."
              className="w-full px-0 py-2 text-sm text-gray-600 border-0 focus:ring-0 focus:outline-none resize-none placeholder:text-gray-400"
              rows={3}
              maxLength={2000}
              disabled={loading}
            />
          </div>

          <div className="flex gap-2 pt-2">
            <button
              onClick={handleSaveEdit}
              disabled={loading || !editTitle.trim()}
              className="px-4 py-2 bg-primary text-white text-sm font-medium rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:shadow-sm"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancelEdit}
              disabled={loading}
              className="px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200 disabled:opacity-50 transition-all duration-200"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="group bg-white rounded-xl border border-gray-200 p-4 transition-all duration-200 hover:shadow-md hover:border-gray-300 animate-in fade-in slide-in-from-bottom-2 duration-300">
      {error && (
        <div className="mb-3 bg-red-50 border-l-4 border-red-400 text-red-700 px-4 py-2 rounded-r text-sm animate-in fade-in slide-in-from-top-1 duration-200">
          {error}
        </div>
      )}

      <div className="flex items-start gap-3">
        {/* Custom Checkbox */}
        <button
          onClick={handleToggleStatus}
          disabled={loading}
          className={`flex-shrink-0 mt-0.5 w-5 h-5 rounded-full border-2 transition-all duration-200 ${
            isCompleted
              ? 'bg-primary border-primary'
              : 'border-gray-300 hover:border-primary'
          } ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'} flex items-center justify-center`}
          aria-label={isCompleted ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {isCompleted && (
            <svg
              className="w-3 h-3 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={3}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-base font-medium transition-all duration-200 ${
              isCompleted
                ? 'line-through text-gray-400'
                : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={`mt-1 text-sm transition-all duration-200 ${
                isCompleted ? 'text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}

          <div className="mt-2 flex items-center gap-3 text-xs text-gray-400">
            <span className="flex items-center gap-1">
              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {new Date(task.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            </span>
            {task.updated_at !== task.created_at && (
              <span className="flex items-center gap-1">
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                {new Date(task.updated_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons - Show on hover */}
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all duration-200"
            title="Edit task"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>

          <button
            onClick={handleDelete}
            disabled={loading}
            className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all duration-200"
            title="Delete task"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
