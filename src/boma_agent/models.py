from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolCall:
    tool_name: str
    tool_input: dict[str, Any]
    output: str
    success: bool = True


@dataclass
class AgentResponse:
    user_query: str
    reasoning: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    answer: str = ""
