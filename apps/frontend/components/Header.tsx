'use client';

import { useRouter } from 'next/navigation';

export default function Header() {
  const router = useRouter();

  const handleLogout = () => {
    // Clear token from localStorage
    localStorage.removeItem('access_token');

    // Clear session cookie
    document.cookie = 'session=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';

    // Redirect to login
    router.push('/login');
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
          </div>

          <div className="flex items-center space-x-4">
            <button
              onClick={handleLogout}
              className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
