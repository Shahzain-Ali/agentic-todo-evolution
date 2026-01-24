'use client';

import { useEffect, useState } from 'react';
import { authenticatedRequest } from '@/lib/api-client';
import type { Task } from '@/lib/definitions';
import TaskCard from './TaskCard';

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      // authenticatedRequest now automatically gets JWT token from Better Auth
      const data = await authenticatedRequest<Task[]>('/api/tasks');
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdate = () => {
    fetchTasks(); // Refresh task list after update
  };

  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-xl border border-gray-200 p-4 animate-pulse">
            <div className="flex items-start gap-3">
              <div className="w-5 h-5 bg-gray-200 rounded-full flex-shrink-0 mt-0.5"></div>
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-400 text-red-700 px-4 py-3 rounded-r animate-in fade-in slide-in-from-top-1 duration-200">
        {error}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-gray-200 p-12 text-center animate-in fade-in zoom-in-95 duration-300">
        <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <svg
            className="w-8 h-8 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
        <p className="text-sm text-gray-500">Get started by creating your first task above.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} onUpdate={handleTaskUpdate} />
      ))}
    </div>
  );
}
