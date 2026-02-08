"""
ChatKit Router - Simplified Version

[Task]: T046
[From]: specs/003-ai-chatbot/spec.md §3 (User Stories), specs/003-ai-chatbot/plan.md §Phase 8

This module provides a basic ChatKit-compatible endpoint that integrates
with OpenAI API directly (ChatKit Python SDK not yet publicly available).
"""

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
import json
import asyncio
from openai import AsyncOpenAI
import os

router = APIRouter()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def stream_chat_response(message: str):
    """Stream chat responses in ChatKit-compatible format"""
    try:
        # Call OpenAI API with streaming
        stream = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant that helps users manage their todo tasks.

You can help users:
- Add new tasks to their todo list
- View all their tasks
- Mark tasks as complete
- Delete tasks
- Search for specific tasks

Always be friendly, concise, and helpful."""
                },
                {"role": "user", "content": message}
            ],
            stream=True,
        )

        # Stream response chunks
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                # Format as Server-Sent Events
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"

        # Send completion signal
        yield f"data: {json.dumps({'done': True})}\n\n"

    except Exception as e:
        print(f"Streaming Error: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


@router.post("/chatkit")
@router.post("/chatkit/")
async def chatkit_endpoint(request: Request):
    """
    Simplified ChatKit endpoint

    Accepts chat requests and returns streaming AI responses.
    Compatible with ChatKit React component expectations.
    """
    try:
        # Parse request body
        body = await request.json()

        # Extract user message (handle different possible formats)
        user_message = body.get("message") or body.get("text") or body.get("content") or str(body)

        # Return streaming response
        return StreamingResponse(
            stream_chat_response(user_message),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    except json.JSONDecodeError:
        # If body is not JSON, try as plain text
        body_bytes = await request.body()
        user_message = body_bytes.decode()

        return StreamingResponse(
            stream_chat_response(user_message),
            media_type="text/event-stream"
        )

    except Exception as e:
        print(f"ChatKit Error: {e}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )
