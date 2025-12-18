"""
Chat API Routes
Endpoints for AI-powered chatbot conversation about heatmap data.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from typing import Dict

from ..models.chat import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ContextResponse
)
from ...services.ollama_service import get_ollama_service
from ...services.data_exporter import get_data_exporter
from ...utils.config import OLLAMA_MODEL

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat/message", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(request: ChatRequest) -> ChatResponse:
    """
    Send user message and receive AI-generated response.

    Builds data context from current heatmap filters, passes to Ollama for analysis,
    and returns AI response with metadata.

    Args:
        request: ChatRequest with message, context, and history

    Returns:
        ChatResponse with AI answer, timestamp, model info

    Raises:
        400: Invalid request parameters
        503: Ollama service unavailable
        500: AI inference failed
    """
    try:
        # Get services
        ollama_service = get_ollama_service()
        data_exporter = get_data_exporter()

        # Check Ollama health first
        health = ollama_service.check_health()
        if health['status'] != 'connected':
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Ollama service is not available. {health.get('error', '')}"
            )

        # Build data context for AI
        month = request.context.month
        hour = request.context.hour
        day_type = request.context.day_type

        # Get data summary (ONLY backend-calculated stats, no raw data)
        summary = data_exporter.get_context_summary(month, hour, day_type)

        # Build complete context - LLM only receives backend-calculated results
        data_context = {
            'month': month,
            'hour': hour,
            'day_type': day_type,
            'summary': summary
        }

        # Prepare conversation history
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.history
        ]

        # Generate AI response
        logger.info(f"Processing message: {request.message[:50]}...")
        result = ollama_service.generate_response(
            user_message=request.message,
            data_context=data_context,
            history=history
        )

        # Build response
        return ChatResponse(
            response=result['response'],
            timestamp=int(datetime.now().timestamp() * 1000),
            model=result['model'],
            tokens_used=result.get('tokens_used', 0)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )


@router.get("/chat/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def check_health() -> HealthResponse:
    """
    Check Ollama service availability and model status.

    Returns:
        HealthResponse with connection status and error details if any
    """
    try:
        ollama_service = get_ollama_service()
        health = ollama_service.check_health()

        # Determine overall status
        overall_status = "ok" if health['status'] == 'connected' else "degraded"

        # GPU available if model is loaded
        gpu_available = health['model_loaded']

        return HealthResponse(
            status=overall_status,
            ollama_status=health['status'],
            model=OLLAMA_MODEL,
            model_loaded=health['model_loaded'],
            gpu_available=gpu_available if health['model_loaded'] else None,
            error=health.get('error'),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="degraded",
            ollama_status="error",
            model=OLLAMA_MODEL,
            model_loaded=False,
            gpu_available=None,
            error=str(e),
            timestamp=datetime.utcnow().isoformat() + "Z"
        )


@router.get("/chat/context", response_model=ContextResponse, status_code=status.HTTP_200_OK)
async def get_context(month: int, hour: int, day_type: str) -> ContextResponse:
    """
    Get current data context for debugging/testing.

    Optional endpoint to inspect data being passed to AI.

    Args:
        month: Month in YYYYMM format
        hour: Hour of day (0-23)
        day_type: "平日" or "假日"

    Returns:
        ContextResponse with metadata and sample data
    """
    try:
        data_exporter = get_data_exporter()

        # Get summary
        summary = data_exporter.get_context_summary(month, hour, day_type)

        # Get sample data (first 50 records)
        data_records = data_exporter.export_to_json(month, hour, day_type)
        total_records = len(data_records)
        sample_records = data_records[:50]

        # Build metadata
        metadata = {
            'total_records': summary['total_records'],
            'query': {
                'month': month,
                'hour': hour,
                'day_type': day_type
            }
        }

        # Note if data was truncated
        note = None
        if total_records > 50:
            note = f"Showing 50 of {total_records} records"

        return ContextResponse(
            metadata=metadata,
            sample_data=sample_records,
            note=note
        )

    except Exception as e:
        logger.error(f"Error getting context: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve context: {str(e)}"
        )
