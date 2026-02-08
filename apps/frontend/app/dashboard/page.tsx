'use client';

import { useState } from 'react';
import Link from 'next/link';
import TaskList from '@/components/TaskList';
import AddTaskForm from '@/components/AddTaskForm';

export default function DashboardPage() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleTaskAdded = () => {
    // Trigger TaskList refresh by changing key
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Welcome Section */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h2 className="text-4xl font-bold text-gray-900 mb-2">
            Today
          </h2>
          <p className="text-gray-600 text-lg">
            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
          </p>
        </div>
        <Link
          href="/chat"
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <span>🤖</span>
          <span>AI Chat</span>
        </Link>
      </div>

      {/* Add Task Form */}
      <AddTaskForm onTaskAdded={handleTaskAdded} />

      {/* Task List */}
      <TaskList key={refreshKey} />
    </div>
  );
}
