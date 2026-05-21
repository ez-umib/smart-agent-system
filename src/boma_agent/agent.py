"""Multi-agent workflow: planning, tool execution, and response formatting."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .models import AgentResponse, ToolCall
from .tools.calculator import CalculatorTool
from .tools.file_reader import FileReaderTool
from .tools.keyword_search import KeywordSearchTool


@dataclass
class ExecutionContext:
    """Shared runtime settings passed to tools during execution."""

    knowledge_base_path: str


class PlannerAgent:
    """Maps free-text user input to an action name and parameters."""

    def create_plan(self, query: str) -> tuple[str, dict[str, str]]:
        lower = query.lower()

        math_pattern = r"[\d\.\+\-\*\/\(\)\%\^ ]+"
        if "calculate" in lower or "math" in lower:
            expression = query.split(":", maxsplit=1)[-1].strip()
            return "calculate", {"expression": expression}
        if re.fullmatch(math_pattern, query.strip()):
            return "calculate", {"expression": query.strip().replace("^", "**")}

        if lower.startswith("read file"):
            path = query.split("read file", maxsplit=1)[-1].strip()
            return "read_file", {"path": path}

        return "search_knowledge", {"question": query}


class ExecutorAgent:
    """Routes planned actions to the matching tool implementation."""

    def __init__(self) -> None:
        self.calculator = CalculatorTool()
        self.file_reader = FileReaderTool()
        self.search_tool = KeywordSearchTool()

    def execute(self, action: str, params: dict[str, str], ctx: ExecutionContext) -> ToolCall:
        if action == "calculate":
            result = self.calculator.run(params["expression"])
            return ToolCall(
                tool_name=self.calculator.name,
                tool_input=params,
                output=result,
            )

        if action == "read_file":
            result = self.file_reader.run(params["path"])
            return ToolCall(
                tool_name=self.file_reader.name,
                tool_input=params,
                output=result,
            )

        if action == "search_knowledge":
            result = self.search_tool.run(params["question"], ctx.knowledge_base_path)
            return ToolCall(
                tool_name=self.search_tool.name,
                tool_input=params,
                output=result,
            )

        raise ValueError(f"Unknown action: {action}")


class SmartAssistant:
    """Orchestrates planning, execution, error handling, and final answers."""

    def __init__(self, knowledge_base_path: str | None = None) -> None:
        base = Path(__file__).resolve().parents[2]
        default_kb = base / "data" / "knowledge_base.txt"
        self.ctx = ExecutionContext(knowledge_base_path=str(knowledge_base_path or default_kb))
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()

    def run(self, query: str) -> AgentResponse:
        action, params = self.planner.create_plan(query)
        reasoning = f"Planned action '{action}' based on user intent."
        response = AgentResponse(user_query=query, reasoning=reasoning)

        try:
            tool_call = self.executor.execute(action, params, self.ctx)
            response.tool_calls.append(tool_call)
            response.answer = self._format_answer(action, tool_call.output)
        except Exception as exc:
            response.tool_calls.append(
                ToolCall(
                    tool_name=action,
                    tool_input=params,
                    output=str(exc),
                    success=False,
                )
            )
            response.answer = f"Request failed: {exc}"
        return response

    def _format_answer(self, action: str, tool_output: str) -> str:
        if action == "calculate":
            return f"Calculation result: {tool_output}"
        if action == "read_file":
            preview = tool_output[:500]
            return f"File content preview:\n{preview}"
        return f"Knowledge answer:\n{tool_output}"
