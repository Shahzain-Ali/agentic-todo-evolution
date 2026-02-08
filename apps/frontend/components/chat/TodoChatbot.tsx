/**
 * Todo Chatbot Component
 *
 * [Task]: T044
 * [From]: specs/003-ai-chatbot/spec.md §3 (User Stories), specs/003-ai-chatbot/plan.md §Phase 8
 *
 * This component provides the AI-powered chat interface for todo management
 * using OpenAI's ChatKit React component.
 */

"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";

export default function TodoChatbot() {
  // Initialize ChatKit with MCP server backend
  const { control } = useChatKit({
    api: {
      url: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
      domainKey: "local-dev",
    },
  });

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 border-b border-blue-800">
        <h2 className="text-xl font-semibold text-white flex items-center gap-2">
          <span>🤖</span>
          <span>AI Todo Assistant</span>
        </h2>
        <p className="text-blue-100 text-sm mt-1">
          Manage your tasks using natural language
        </p>
      </div>

      {/* ChatKit Component */}
      <ChatKit control={control} className="h-[600px] w-full" />
    </div>
  );
}
