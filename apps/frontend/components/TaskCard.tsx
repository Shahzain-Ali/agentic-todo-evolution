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
  const [isHovered, setIsHovered] = useState(false);

  const handleToggleStatus = async () => {
    setLoading(true);
    setError('');

    try {
      const newStatus = isCompleted ? 'pending' : 'completed';
      const updateData: TaskUpdate = { status: newStatus };

      // authenticatedRequest now automatically gets JWT token from Better Auth
      await authenticatedRequest(`/api/tasks/${task.id}`, {
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
      const updateData: TaskUpdate = {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      };

      // authenticatedRequest now automatically gets JWT token from Better Auth
      await authenticatedRequest(`/api/tasks/${task.id}`, {
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
    const confirmed = window.confirm(
      `Delete "${task.title}"?`
    );

    if (!confirmed) {
      return;
    }

    setLoading(true);
    setError('');

    try {
      // authenticatedRequest now automatically gets JWT token from Better Auth
      await authenticatedRequest(`/api/tasks/${task.id}`, {
        method: 'DELETE',
      });

      onUpdate();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      setLoading(false);
    }
  };

  if (isEditing) {
    return (
      <div className="group bg-white rounded-2xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-all duration-300 animate-in fade-in slide-in-from-top-3">
        {error && (
          <div className="mb-4 bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded-lg text-sm flex items-center gap-2">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}

        <div className="space-y-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            placeholder="Task title"
            className="w-full px-0 py-3 text-lg font-semibold text-gray-900 border-0 border-b-2 border-gray-200 focus:border-primary focus:ring-0 focus:outline-none transition-colors placeholder:text-gray-400"
            maxLength={200}
            disabled={loading}
            autoFocus
          />

          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            placeholder="Add more details..."
            className="w-full px-0 py-2 text-base text-gray-600 border-0 focus:ring-0 focus:outline-none resize-none placeholder:text-gray-400"
            rows={3}
            maxLength={2000}
            disabled={loading}
          />

          <div className="flex gap-3 pt-3 border-t border-gray-100">
            <button
              onClick={handleSaveEdit}
              disabled={loading || !editTitle.trim()}
              className="px-6 py-2.5 bg-primary text-white text-sm font-semibold rounded-xl hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-lg shadow-primary/20 hover:shadow-xl hover:scale-105"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancelEdit}
              disabled={loading}
              className="px-6 py-2.5 bg-gray-100 text-gray-700 text-sm font-semibold rounded-xl hover:bg-gray-200 disabled:opacity-50 transition-all duration-200"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`group bg-white rounded-2xl border transition-all duration-300 hover:shadow-lg ${
        isCompleted
          ? 'border-gray-200/50 bg-gray-50/50'
          : 'border-gray-200 hover:border-primary/20'
      } animate-in fade-in slide-in-from-bottom-3`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {error && (
        <div className="mx-6 mt-4 mb-2 bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded-lg text-sm flex items-center gap-2">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          {error}
        </div>
      )}

      <div className="flex items-start gap-4 p-6">
        {/* Custom Checkbox */}
        <button
          onClick={handleToggleStatus}
          disabled={loading}
          className={`flex-shrink-0 mt-0.5 w-6 h-6 rounded-full border-2 transition-all duration-300 ${
            isCompleted
              ? 'bg-primary border-primary shadow-lg shadow-primary/20'
              : 'border-gray-300 hover:border-primary hover:scale-110'
          } ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'} flex items-center justify-center group-hover:scale-110`}
          aria-label={isCompleted ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {isCompleted && (
            <svg
              className="w-4 h-4 text-white animate-in zoom-in duration-200"
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
            className={`text-base font-semibold leading-relaxed transition-all duration-300 ${
              isCompleted
                ? 'line-through text-gray-400'
                : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p
              className={`mt-2 text-sm leading-relaxed transition-all duration-300 ${
                isCompleted ? 'text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}

          <div className="mt-3 flex items-center gap-4 text-xs text-gray-400">
            <span className="flex items-center gap-1.5">
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {new Date(task.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            </span>
            {task.updated_at !== task.created_at && (
              <span className="flex items-center gap-1.5 px-2 py-1 bg-gray-100 rounded-lg">
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Edited
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className={`flex items-center gap-2 transition-all duration-300 ${
          isHovered ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-2'
        }`}>
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className="p-2.5 text-gray-400 hover:text-primary hover:bg-primary/5 rounded-xl transition-all duration-200"
            title="Edit task"
          >
            <svg
              className="w-5 h-5"
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
            className="p-2.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200"
            title="Delete task"
          >
            <svg
              className="w-5 h-5"
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
