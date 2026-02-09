"use client";

import { useState } from "react";

export default function FloatingChatWidget() {
  const [isOpen, setIsOpen] = useState(false);

  // Agent Builder workflow URL
  const AGENT_BUILDER_URL = "https://platform.openai.com/playground/workflows/wf_698889a8c8188190b54b40ef2682acd00dbcf4a7ca7f9876";

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-full p-4 shadow-2xl transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-4 focus:ring-blue-300"
        aria-label="Open AI Chat Assistant"
      >
        {isOpen ? (
          // Close icon
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        ) : (
          // Chat icon
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        )}
      </button>

      {/* Modal/Drawer */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-96 h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🤖</span>
              <div>
                <h3 className="text-white font-semibold text-lg">AI Todo Assistant</h3>
                <p className="text-blue-100 text-xs">Manage tasks naturally</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-blue-800 rounded-full p-1 transition"
              aria-label="Close chat"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          {/* Agent Builder Iframe */}
          <div className="flex-1 overflow-hidden">
            <iframe
              src={AGENT_BUILDER_URL}
              className="w-full h-full border-0"
              title="AI Todo Assistant"
              sandbox="allow-same-origin allow-scripts allow-forms allow-popups"
            />
          </div>

          {/* Footer hint */}
          <div className="bg-gray-50 px-4 py-2 text-center text-xs text-gray-500 border-t">
            Powered by OpenAI Agent Builder
          </div>
        </div>
      )}
    </>
  );
}
