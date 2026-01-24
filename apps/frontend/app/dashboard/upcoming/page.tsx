'use client';

import { useState, useEffect } from 'react';
import { authenticatedRequest } from '@/lib/api-client';
import TaskCard from '@/components/TaskCard';
import type { Task } from '@/lib/definitions';

export default function UpcomingPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchUpcomingTasks();
  }, []);

  const fetchUpcomingTasks = async () => {
    try {
      setLoading(true);
      // Use authenticatedRequest which handles JWT tokens automatically
      const data = await authenticatedRequest<Task[]>('/api/tasks');
      // Filter only incomplete tasks (upcoming)
      const upcomingTasks = data.filter((task: Task) => task.status === 'pending');
      setTasks(upcomingTasks);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">Upcoming</h2>
          <p className="text-gray-600 text-lg">Your pending tasks</p>
        </div>
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">Upcoming</h2>
          <p className="text-gray-600 text-lg">Your pending tasks</p>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header Section */}
      <div className="mb-8">
        <h2 className="text-4xl font-bold text-gray-900 mb-2">Upcoming</h2>
        <p className="text-gray-600 text-lg">
          {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} to complete
        </p>
      </div>

      {/* Task List */}
      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
            <svg
              className="w-8 h-8 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-1">
            No upcoming tasks
          </h3>
          <p className="text-gray-600">
            All your tasks are completed!
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onUpdate={fetchUpcomingTasks}
            />
          ))}
        </div>
      )}
    </div>
  );
}
