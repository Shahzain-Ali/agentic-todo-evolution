'use client';

import { useState } from 'react';
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
      <div className="mb-8">
        <h2 className="text-4xl font-bold text-gray-900 mb-2">
          Today
        </h2>
        <p className="text-gray-600 text-lg">
          {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
        </p>
      </div>

      {/* Add Task Form */}
      <AddTaskForm onTaskAdded={handleTaskAdded} />

      {/* Task List */}
      <TaskList key={refreshKey} />
    </div>
  );
}
