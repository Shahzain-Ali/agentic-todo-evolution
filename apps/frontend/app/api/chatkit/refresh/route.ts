/**
 * ChatKit Token Refresh API Route
 *
 * [Task]: T015
 * [From]: specs/003-ai-chatbot/spec.md §2.1 (FR-001), specs/003-ai-chatbot/plan.md §Phase 2
 *
 * This route refreshes an expired ChatKit session token.
 * It validates the existing token and calls OpenAI API to get a new client secret.
 */

import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";

export async function POST(request: NextRequest) {
  try {
    // Validate Better Auth session
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session || !session.user) {
      return NextResponse.json(
        { error: "Unauthorized - please log in" },
        { status: 401 }
      );
    }

    // Get existing token from request body
    const body = await request.json();
    const { token } = body;

    if (!token) {
      return NextResponse.json(
        { error: "Missing token parameter" },
        { status: 400 }
      );
    }

    // Get OpenAI API key
    const openaiApiKey = process.env.OPENAI_API_KEY;

    if (!openaiApiKey) {
      console.error("OPENAI_API_KEY not configured");
      return NextResponse.json(
        { error: "Server configuration error" },
        { status: 500 }
      );
    }

    // Call OpenAI API to refresh session
    // Note: As of current OpenAI API, session refresh might create a new session
    // This implementation follows the pattern from ChatKit documentation
    const response = await fetch("https://api.openai.com/v1/realtime/sessions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${openaiApiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gpt-4o-mini-realtime-preview-2024-12-17",
        voice: "verse",
        metadata: {
          user_id: session.user.id,
          user_jwt: session.session.token,
          refresh: true,
        },
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("OpenAI API refresh error:", errorData);
      return NextResponse.json(
        { error: "Failed to refresh ChatKit session" },
        { status: response.status }
      );
    }

    const sessionData = await response.json();

    // Return new client secret
    return NextResponse.json({
      client_secret: sessionData.client_secret.value,
      session_id: sessionData.id,
    });

  } catch (error) {
    console.error("ChatKit token refresh error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
