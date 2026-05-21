"""CLI entry point for the Smart Agent System."""

from __future__ import annotations

import argparse
import json

from .agent import SmartAssistant


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smart-assistant",
        description="AI-assisted tool-using agent demo project.",
    )
    parser.add_argument("--query", required=True, help="User request for the assistant.")
    parser.add_argument(
        "--knowledge-base",
        default=None,
        help="Optional path to a knowledge base text file.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    assistant = SmartAssistant(knowledge_base_path=args.knowledge_base)
    result = assistant.run(args.query)
    print(
        json.dumps(
            {
                "user_query": result.user_query,
                "reasoning": result.reasoning,
                "tool_calls": [
                    {
                        "tool_name": call.tool_name,
                        "tool_input": call.tool_input,
                        "output": call.output,
                        "success": call.success,
                    }
                    for call in result.tool_calls
                ],
                "answer": result.answer,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
