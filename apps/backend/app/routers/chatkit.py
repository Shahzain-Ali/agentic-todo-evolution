"""
ChatKit Router - Agent Builder Integration

[Task]: T046
[From]: specs/003-ai-chatbot/spec.md §3 (User Stories), specs/003-ai-chatbot/plan.md §Phase 8

This module provides ChatKit session endpoints that integrate with OpenAI Agent Builder workflow.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from openai import AsyncOpenAI
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Agent Builder Workflow ID
WORKFLOW_ID = "wf_698889a8c8188190b54b40ef2682acd00dbcf4a7ca7f9876"


@router.post("/chatkit/session")
async def create_session():
    """
    Create a new ChatKit session with Agent Builder workflow

    Returns:
        JSON with client_secret for ChatKit initialization
    """
    try:
        logger.info(f"Creating ChatKit session for workflow: {WORKFLOW_ID}")

        # Create session with OpenAI Realtime API (without workflow parameter)
        response = await client.beta.realtime.sessions.create(
            model="gpt-4o-mini"
        )

        logger.info(f"Session created successfully: {response.id}")

        return JSONResponse({
            "client_secret": response.client_secret.value,
            "session_id": response.id,
            "workflow_id": WORKFLOW_ID  # Pass workflow ID to frontend
        })

    except Exception as e:
        logger.error(f"Error creating ChatKit session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.post("/chatkit/refresh")
async def refresh_session(token: str = None):
    """
    Refresh an existing ChatKit session

    For now, just creates a new session (OpenAI handles token refresh internally)
    """
    try:
        logger.info("Refreshing ChatKit session")

        # Create new session (OpenAI ChatKit handles refresh internally)
        response = await client.beta.realtime.sessions.create(
            model="gpt-4o-mini"
        )

        return JSONResponse({
            "client_secret": response.client_secret.value,
            "session_id": response.id,
            "workflow_id": WORKFLOW_ID
        })

    except Exception as e:
        logger.error(f"Error refreshing ChatKit session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to refresh session: {str(e)}")
