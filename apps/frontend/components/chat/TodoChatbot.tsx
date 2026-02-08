/**
 * Todo Chatbot Component - OpenAI Hosted ChatKit
 *
 * [Task]: T044
 * [From]: specs/003-ai-chatbot/spec.md §3 (User Stories), specs/003-ai-chatbot/plan.md §Phase 8
 *
 * This component uses OpenAI's hosted ChatKit with client secret authentication.
 */

"use client";

import { ChatKit, useChatKit } from "@openai/chatkit-react";

export default function TodoChatbot() {
  // Initialize ChatKit with OpenAI-hosted backend using getClientSecret
  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        // If we have an existing secret and it's not expired, refresh it
        if (existing) {
          const res = await fetch('/api/chatkit/refresh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: existing }),
          });
          const data = await res.json();
          return data.client_secret;
        }

        // Otherwise, create a new ChatKit session
        const res = await fetch('/api/chatkit/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        const data = await res.json();
        return data.client_secret;
      },
    },
    // Customize the start screen
    startScreen: {
      greeting: "Hello! I'm your AI Todo Assistant 🤖",
      prompts: [
        {
          label: "Add a task",
          prompt: "Add buy groceries to my list",
          icon: "plus",
        },
        {
          label: "View tasks",
          prompt: "Show me all my tasks",
          icon: "list",
        },
        {
          label: "Complete a task",
          prompt: "Mark task 1 as done",
          icon: "check",
        },
      ],
    },
    composer: {
      placeholder: "Ask me to add, view, or complete tasks...",
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
