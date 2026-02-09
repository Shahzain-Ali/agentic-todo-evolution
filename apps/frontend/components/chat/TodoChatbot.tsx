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
  // Initialize ChatKit with public key and workflow
  const { control } = useChatKit({
    publicKey: "domain_pk_698988637f4c8193a082e64ba7ca1a1f074f25075ca05848",
    workflowId: "wf_698889a8c8188190b54b40ef2682acd00dbcf4a7ca7f9876",
    startScreen: {
      greeting: "Hello! I'm your AI Todo Assistant 🤖",
      prompts: [
        {
          label: "Add a task",
          prompt: "Add buy groceries to my list",
        },
        {
          label: "View tasks",
          prompt: "Show me all my tasks",
        },
        {
          label: "Complete a task",
          prompt: "Mark task 1 as done",
        },
      ],
    },
    composer: {
      placeholder: "Ask me to add, view, or complete tasks...",
    },
  } as any);

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
