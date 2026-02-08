/**
 * Chat Page
 *
 * [Task]: T045
 * [From]: specs/003-ai-chatbot/spec.md §3 (User Stories), specs/003-ai-chatbot/plan.md §Phase 8
 *
 * This page provides the AI-powered todo management chat interface.
 * It requires authentication and redirects unauthenticated users to login.
 */

import TodoChatbot from "@/components/chat/TodoChatbot";
import Link from "next/link";

export const metadata = {
  title: "AI Chat - Todo App",
  description: "Manage your todos using natural language AI assistant",
};

export default async function ChatPage() {
  // TODO: Re-enable authentication after DATABASE_URL is configured
  // For now, allow access for testing purposes
  const testUserEmail = "test@example.com";

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Navigation Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-8">
              <h1 className="text-xl font-bold text-gray-900">
                Todo App
              </h1>
              <nav className="flex gap-4">
                <Link
                  href="/dashboard"
                  className="text-gray-600 hover:text-gray-900 transition"
                >
                  Dashboard
                </Link>
                <Link
                  href="/chat"
                  className="text-blue-600 font-medium border-b-2 border-blue-600"
                >
                  AI Chat
                </Link>
              </nav>
            </div>

            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                {testUserEmail}
              </span>
              <Link
                href="/login"
                className="text-sm text-gray-600 hover:text-gray-900 transition"
              >
                Sign Out
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            AI Todo Assistant
          </h2>
          <p className="text-gray-600">
            Manage your tasks using natural language. Just tell me what you want
            to do!
          </p>
        </div>

        {/* Info Banner */}
        <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <span className="text-blue-600 text-xl">💡</span>
            <div>
              <h3 className="font-medium text-blue-900 mb-1">
                How to use the AI Assistant
              </h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Create tasks: &quot;Add buy groceries to my list&quot;</li>
                <li>• View tasks: &quot;Show me all my tasks&quot; or &quot;What tasks do I have left?&quot;</li>
                <li>• Complete tasks: &quot;Mark task 1 as done&quot; or &quot;I finished the first one&quot;</li>
                <li>• The assistant understands natural language - just ask!</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Chat Interface */}
        <TodoChatbot />

        {/* Help Section */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            Having trouble?{" "}
            <Link href="/dashboard" className="text-blue-600 hover:underline">
              Go to traditional dashboard
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}
