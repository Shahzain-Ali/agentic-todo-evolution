/**
 * ChatKit Session API Route
 *
 * [Task]: T014
 * [From]: specs/003-ai-chatbot/spec.md §2.1 (FR-001), specs/003-ai-chatbot/plan.md §Phase 2
 *
 * This route creates a new ChatKit session for authenticated users.
 * It validates the user's Better Auth session and calls OpenAI API to create
 * a ChatKit client secret.
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

    // Get user JWT token from session (needed for MCP tool authentication)
    const userJWT = session.session.token; // Better Auth provides JWT token

    // Create ChatKit session via OpenAI API
    const openaiApiKey = process.env.OPENAI_API_KEY;

    if (!openaiApiKey) {
      console.error("OPENAI_API_KEY not configured");
      return NextResponse.json(
        { error: "Server configuration error" },
        { status: 500 }
      );
    }

    // Call OpenAI API to create ChatKit session
    const response = await fetch("https://api.openai.com/v1/realtime/sessions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${openaiApiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gpt-4o-mini-realtime-preview-2024-12-17",
        voice: "verse",
        // Pass user JWT in metadata for MCP tool authentication
        metadata: {
          user_id: session.user.id,
          user_jwt: userJWT,
        },
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("OpenAI API error:", errorData);
      return NextResponse.json(
        { error: "Failed to create ChatKit session" },
        { status: response.status }
      );
    }

    const sessionData = await response.json();

    // Return client secret to frontend
    return NextResponse.json({
      client_secret: sessionData.client_secret.value,
      session_id: sessionData.id,
    });

  } catch (error) {
    console.error("ChatKit session creation error:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
