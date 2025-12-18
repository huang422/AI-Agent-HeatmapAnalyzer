"""
Chat API Models
Pydantic models for chat endpoints request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime


class ChatMessage(BaseModel):
    """Single message in conversation history."""
    role: Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1, max_length=10000)
    timestamp: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "哪個時段最繁忙？",
                "timestamp": 1734480123456
            }
        }


class DataContext(BaseModel):
    """Current heatmap filter context."""
    month: int = Field(..., description="YYYYMM format (e.g., 202412)")
    hour: int = Field(..., ge=0, le=23, description="Hour of day (0-23)")
    day_type: Literal["平日", "假日"] = Field(..., description="Day type: weekday or weekend")

    @field_validator('month')
    @classmethod
    def validate_month(cls, v):
        """Validate month format."""
        if not (100000 <= v <= 999912):
            raise ValueError("Month must be in YYYYMM format (e.g., 202412)")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "month": 202412,
                "hour": 8,
                "day_type": "平日"
            }
        }


class ChatRequest(BaseModel):
    """Request body for POST /api/chat/message."""
    message: str = Field(..., min_length=1, max_length=500, description="User's question")
    context: DataContext = Field(..., description="Current heatmap filter conditions")
    history: List[ChatMessage] = Field(default_factory=list, max_length=20, description="Recent conversation history")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "哪個時段最繁忙？",
                "context": {
                    "month": 202412,
                    "hour": 8,
                    "day_type": "平日"
                },
                "history": []
            }
        }


class ChatResponse(BaseModel):
    """Response body for POST /api/chat/message."""
    response: str = Field(..., description="AI-generated answer")
    timestamp: int = Field(..., description="Unix timestamp (ms) of response generation")
    model: str = Field(..., description="Model used (e.g., qwen2.5:7b)")
    tokens_used: int = Field(default=0, description="Approximate token count")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "根據12月平日早上8點的數據，此時段總使用者數為5234.5人...",
                "timestamp": 1734480123456,
                "model": "qwen2.5:7b",
                "tokens_used": 245
            }
        }


class HealthResponse(BaseModel):
    """Response body for GET /api/chat/health."""
    status: Literal["ok", "degraded"] = Field(..., description="Overall service status")
    ollama_status: Literal["connected", "disconnected", "error"] = Field(..., description="Ollama connection state")
    model: str = Field(..., description="Expected model name")
    model_loaded: bool = Field(..., description="Whether model is available")
    gpu_available: Optional[bool] = Field(None, description="GPU acceleration status")
    error: Optional[str] = Field(None, description="Error message if any")
    timestamp: str = Field(..., description="ISO 8601 timestamp of health check")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "ollama_status": "connected",
                "model": "qwen2.5:7b",
                "model_loaded": True,
                "gpu_available": True,
                "error": None,
                "timestamp": "2025-12-17T10:30:00Z"
            }
        }


class ContextResponse(BaseModel):
    """Response body for GET /api/chat/context (debug endpoint)."""
    metadata: dict = Field(..., description="Summary of filtered data")
    sample_data: List[dict] = Field(..., description="Sample data records (max 50)")
    note: Optional[str] = Field(None, description="Informational message")

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {
                    "total_records": 124,
                    "query": {"month": 202412, "hour": 8, "day_type": "平日"}
                },
                "sample_data": [],
                "note": "Showing 50 of 124 records"
            }
        }
