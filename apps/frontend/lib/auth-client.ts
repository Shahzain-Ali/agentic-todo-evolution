/**
 * Better Auth Client Configuration
 *
 * This file initializes the Better Auth client for the frontend application.
 * It connects to the FastAPI backend authentication endpoints.
 *
 * Official Docs: https://www.better-auth.com/docs/installation
 * Context7 Library: /llmstxt/better-auth_llms_txt
 */

import { createAuthClient } from "better-auth/react";

/**
 * Auth Client Instance
 *
 * Configured to communicate with FastAPI backend on port 8001.
 * The baseURL points to the backend API, where Better Auth will send
 * authentication requests (signUp, signIn, signOut, session management).
 */
/**
 * Get the base URL for authentication
 * - In browser: use window.location.origin
 * - In server: use environment variable
 */
const getBaseURL = () => {
  if (typeof window !== 'undefined') {
    // Client-side: use current origin
    return window.location.origin;
  }
  // Server-side: use environment variable
  return process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';
};

export const authClient = createAuthClient({
  /**
   * Base URL of the authentication server (Next.js)
   * Must be an ABSOLUTE URL (Better Auth requirement)
   *
   * Better Auth will append /api/auth/sign-up/email etc. to this baseURL
   * The Next.js API route then forwards to FastAPI backend
   */
  baseURL: getBaseURL(),
});

/**
 * Export authentication methods for easy importing in components
 *
 * Usage in components:
 * ```typescript
 * import { authClient } from "@/lib/auth-client";
 *
 * // Sign up
 * await authClient.signUp.email({
 *   email: "user@example.com",
 *   password: "password123",
 *   name: "John Doe"
 * });
 *
 * // Sign in
 * await authClient.signIn.email({
 *   email: "user@example.com",
 *   password: "password123"
 * });
 *
 * // Sign out
 * await authClient.signOut();
 * ```
 */
export const { signIn, signUp, signOut, useSession } = authClient;
