/**
 * Better Auth Server Configuration
 *
 * Server-side Better Auth instance for API routes and Server Components.
 * Used for session validation in protected routes.
 */

import { betterAuth } from "better-auth";

export const auth = betterAuth({
  /**
   * Database configuration
   * Better Auth needs database access for session management
   */
  database: {
    provider: "pg", // PostgreSQL
    url: process.env.DATABASE_URL || "",
  },

  /**
   * Secret key for signing JWTs
   */
  secret: process.env.BETTER_AUTH_SECRET || process.env.SECRET_KEY || "",

  /**
   * Base URL for the application
   */
  baseURL: process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000",
});
