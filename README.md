# Boma Agent System

This repository contains a practical Python implementation of an AI-assisted, tool-using agent workflow.

## What the system does

The system accepts a user query and solves it through an agent pipeline:

1. `PlannerAgent` identifies the task type.
2. `ExecutorAgent` calls a suitable tool.
3. `BomaAssistant` returns a structured result with reasoning, tool calls, and final answer.

Supported flows:

- math evaluation via `CalculatorTool`,
- file reading via `FileReaderTool`,
- local knowledge lookup via `KeywordSearchTool`.

## Project structure

- `src/boma_agent/` - source code
- `src/boma_agent/tools/` - tool implementations
- `tests/` - functional tests
- `data/` - local data for tool usage
- `requirements.txt` - testing dependency
- `pyproject.toml` - package metadata
- `JOURNAL.md` - submission-stage notes
- `REPORT.md` - full implementation/testing/deployment report

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Run

Example math request:

```bash
python -m boma_agent.main --query "4 + 5 * 2"
```

Example file read request:

```bash
python -m boma_agent.main --query "read file data/sample_notes.txt"
```

Example knowledge request:

```bash
python -m boma_agent.main --query "How do I run tests?"
```

## Testing

```bash
pytest -q
```

## Input, conversion, and consistency

- Input is plain text from CLI (`--query`).
- Planner converts text intent into a normalized action and parameters.
- Tools return raw outputs (numbers, file text, matched lines).
- Assistant converts raw tool output into a stable response schema:
  - `user_query`
  - `reasoning`
  - `tool_calls` (with `tool_name`, input, output, success)
  - `answer`
- This consistent schema ensures data portability between components.

## Deployment preparation

The current deployment target is a local CLI application:

- lightweight and easy to install,
- deterministic and testable,
- suitable for controlled staged release (dev -> test -> production machine).

Future deployment options:

- wrap as REST API service,
- package with Docker,
- add CI pipeline for automated tests on push.

## Environment variables

No environment variables are required in this version.

## Submission documents

- `JOURNAL.md` contains Step 1 (24.04) journal requirements in English.
- `REPORT.md` contains full implementation-phase evidence for later submission stages.
