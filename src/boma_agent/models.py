"""Structured response models for the agent workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    """Record of one tool invocation during assistant execution."""
    tool_name: str
    tool_input: dict[str, Any]
    output: str
    success: bool = True


@dataclass
class AgentResponse:
    """JSON-serializable assistant result with reasoning and tool trace."""

    user_query: str
    reasoning: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    answer: str = ""
