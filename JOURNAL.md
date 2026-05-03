# Journal

## Step 1 - 24.04

### Planned system and goal

The planned system is a Python command-line assistant named **Smart Agent System**.
Its goal is to receive user requests and solve practical tasks through an agent workflow that uses tools during execution.

### AI / agent-based approach

The architecture uses an agent workflow with separated responsibilities:

- **PlannerAgent** interprets user intent and selects an action.
- **ExecutorAgent** executes the selected action by calling a concrete tool.
- **SmartAssistant** orchestrates planning, execution, error handling, and final response formatting.

This creates a practical intelligent-agent pattern with explicit tool use.

### Tools used in the system

1. **CalculatorTool** - safe arithmetic evaluation.
2. **FileReaderTool** - reads local file content for analysis or preview.
3. **KeywordSearchTool** - retrieves relevant lines from a local knowledge base.

### Preliminary programming concepts required

- Python package structure and modularization
- Classes, dataclasses, and dependency composition
- CLI input/output with `argparse`
- Tool abstraction and execution routing
- Error handling and input validation
- File I/O and text processing
- Automated testing with `pytest`
- Version control workflow with Git and meaningful commits

## Step 2 - Updated based on implementation progress

### Updated system description

The implemented system is a working Python CLI agent called **Smart Agent System** that accepts user requests through `--query` and resolves them through a 3-stage flow:

1. **Planning** (`PlannerAgent`) classifies the request as `calculate`, `read_file`, or `search_knowledge`.
2. **Execution** (`ExecutorAgent`) routes the action to the matching tool.
3. **Response orchestration** (`SmartAssistant`) returns a structured output containing reasoning, tool-call trace, and final answer.

At runtime, the system currently supports:

- safe arithmetic evaluation,
- local file reading with validation and truncation,
- keyword-based lookup in a local knowledge base.

The output format is stable JSON with:

- `user_query`
- `reasoning`
- `tool_calls` (`tool_name`, `tool_input`, `output`, `success`)
- `answer`

### Refined programming concepts actually used

- **Modular architecture** with package-based separation (`agent`, `models`, `tools`, `main`)
- **Object-oriented design** (separate agent and tool classes)
- **Dataclasses** for structured response models (`ToolCall`, `AgentResponse`, `ExecutionContext`)
- **Intent parsing and routing** with simple NLP heuristics (`lower()`, regex, prefix checks)
- **Safe expression evaluation** using `ast` + operator whitelisting
- **File/path handling** using `pathlib.Path` and UTF-8 reads
- **Validation and exception handling** (`ValueError`, `FileNotFoundError`, fallback error response)
- **CLI interface design** with `argparse`
- **JSON serialization** for standardized machine-readable output
- **Automated tests** with `pytest` covering workflow and tool-level behavior

### How these concepts are applied in this project

- **Separation of concerns:** planning, execution, and formatting are isolated to keep logic maintainable and testable.
- **Datamodel consistency:** `ToolCall` and `AgentResponse` enforce a predictable schema that can be reused by future API or UI layers.
- **Routing logic:** planner converts free-text user input into normalized action + parameter dictionaries for the executor.
- **Security-oriented computation:** calculator accepts only allowed AST node/operator types, preventing unsafe evaluation.
- **Robust I/O behavior:** file tool validates path existence/type before reading and truncates long outputs for controlled responses.
- **Resilient assistant flow:** execution errors are captured and included in response trace instead of crashing the program.
- **Test-driven confidence:** tests validate both happy paths and invalid input behavior, protecting against regressions.

### How tools are integrated into the system

Tools are integrated through a clear adapter pattern inside `ExecutorAgent`:

- `CalculatorTool.run(expression)` for math requests
- `FileReaderTool.run(path)` for `read file ...` requests
- `KeywordSearchTool.run(question, knowledge_base_path)` for knowledge queries

Integration details:

- `ExecutorAgent` instantiates tools once and maps action names to tool calls.
- `SmartAssistant` passes shared runtime context (knowledge-base path) via `ExecutionContext`.
- Every tool invocation is recorded as a `ToolCall` entry and attached to final output.
- `main.py` exposes integration to end users by parsing CLI arguments and printing JSON.

This integration keeps the system extensible: a new tool can be added by implementing a new class and adding one routing branch in planner/executor.
