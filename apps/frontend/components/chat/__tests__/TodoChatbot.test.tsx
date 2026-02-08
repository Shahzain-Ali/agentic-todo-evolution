/**
 * Tests for TodoChatbot Component
 *
 * [Task]: T046
 * [From]: specs/003-ai-chatbot/spec.md §Success Criteria, specs/003-ai-chatbot/plan.md §Testing Strategy
 *
 * Tests cover:
 * - Component rendering
 * - Session creation
 * - Message sending
 * - Error handling
 */

import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import TodoChatbot from "../TodoChatbot";

// Mock ChatKit hook
vi.mock("@openai/chatkit-react", () => ({
  useChatKit: vi.fn(() => ({
    messages: [],
    sendMessage: vi.fn(),
    isLoading: false,
  })),
}));

// Mock fetch
global.fetch = vi.fn();

describe("TodoChatbot", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock successful session creation
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({ client_secret: "test-secret-123" }),
    });
  });

  it("should render loading state initially", () => {
    render(<TodoChatbot />);
    expect(screen.getByText(/initializing chat/i)).toBeInTheDocument();
  });

  it("should create chat session on mount", async () => {
    render(<TodoChatbot />);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "/api/chatkit/session",
        expect.objectContaining({
          method: "POST",
        })
      );
    });
  });

  it("should render start screen when no messages", async () => {
    render(<TodoChatbot />);

    await waitFor(() => {
      expect(screen.getByText(/AI Todo Assistant/i)).toBeInTheDocument();
    });
  });

  it("should display error when session creation fails", async () => {
    // Mock failed session creation
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 500,
    });

    render(<TodoChatbot />);

    await waitFor(() => {
      expect(screen.getByText(/chat unavailable/i)).toBeInTheDocument();
    });
  });

  it("should render suggested prompts", async () => {
    render(<TodoChatbot />);

    await waitFor(() => {
      expect(screen.getByText(/create a task/i)).toBeInTheDocument();
      expect(screen.getByText(/view my tasks/i)).toBeInTheDocument();
    });
  });

  it("should have message input field", async () => {
    render(<TodoChatbot />);

    await waitFor(() => {
      const input = screen.getByPlaceholderText(/type your message/i);
      expect(input).toBeInTheDocument();
    });
  });
});
