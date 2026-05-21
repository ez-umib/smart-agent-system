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

## Step 2 - 08.05

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

## Step 3 - 15.05

### Description of the testing process

Testing was done together with implementation using `pytest`, not only at the end of the project. The process has two layers:

1. **Tool-level tests** (`tests/test_tools.py`) — each tool is checked in isolation (calculator, file reader, keyword search) so bugs are found before integration.
2. **Workflow tests** (`tests/test_agent.py`) — `SmartAssistant` is run end-to-end to verify planning, tool routing, and final answer formatting.

During development, tests were run after changes with:

```bash
pytest -q
```

The suite covers functional workflow behavior, direct tool behavior, and integration between planner, executor, and response models. Input validation is enforced inside tools (for example empty or unsafe expressions, missing files). Error handling is verified at the assistant level: if a tool raises an exception, `SmartAssistant` records a failed `ToolCall` (`success=False`) and returns a readable error in `answer` instead of terminating the program.

Current result: **10 tests passed** in the latest run (including validation and error-handling cases).

### Test scenarios (list and explanation)

| # | Scenario | Purpose | Expected result |
|---|----------|---------|-----------------|
| 1 | Math workflow (`4 + 5 * 2`) | Functional test of planner → calculator → answer | `tool_name` is `calculator`; answer contains `14.0` |
| 2 | File workflow (`read file <path>`) | Functional test of file routing and content return | `tool_name` is `file_reader`; answer contains file text |
| 3 | Knowledge workflow (`How do I test with pytest?`) | Functional test of keyword search with a custom KB | `tool_name` is `keyword_search`; answer mentions `pytest` |
| 4 | Calculator tool (`2 + 3 * 4`) | Tool test without full agent path | Direct output `14.0` |
| 5 | File reader tool (existing temp file) | Tool test for valid UTF-8 read | Returns exact file content |
| 6 | Keyword search tool (sample corpus) | Tool test for ranking/matching lines | Result contains `pytest` |
| 7 | Empty calculator expression | Input validation test | `ValueError` raised |
| 8 | Unsafe calculator expression | Input validation test | `ValueError` raised (AST whitelist) |
| 9 | Missing file (tool level) | Input validation test | `FileNotFoundError` raised |
| 10 | Missing file via workflow | Error handling test | `success=False`, error message in `answer` |

Scenarios 1–3 prove the main agent workflow. Scenarios 4–6 prove each connected tool works correctly on its own. Scenarios 7–10 prove validation and graceful failure behavior. Temporary files (`tmp_path`) are used in tests so results are reproducible on any machine.

### Deployment preparation (how the system can be run)

The system is prepared as a **local installable CLI application**. Another user can run it in a controlled environment with:

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt` and install the package in editable mode (`pip install -e .`).
3. Launch with `python -m boma_agent.main --query "<request>"`.

Optional argument: `--knowledge-base` to point to a custom knowledge file (default: `data/knowledge_base.txt`).

No environment variables are required in this version. Configuration is limited to CLI arguments and packaged data under `data/`. Full install and usage steps are documented in `README.md`; extended deployment notes are in `REPORT.md`.

### Data conversion and porting

The system uses external text data (local files and a knowledge base). Data moves through these stages:

| Stage | Format | Conversion / adaptation |
|-------|--------|-------------------------|
| User input | Plain text (`--query`) | Planner normalizes intent to an internal action (`calculate`, `read_file`, `search_knowledge`) and parameter dict |
| Tool input | Structured parameters (`expression`, `path`, `question`) | Strings extracted via heuristics/regex; math `^` converted to `**` for evaluation |
| Tool output | Raw string (number, file text, matched lines) | File reader truncates very long content; keyword search returns top matching lines |
| Final output | JSON (`AgentResponse`) | Assistant wraps tool output into `reasoning`, `tool_calls`, and human-readable `answer` |

Consistency is preserved by:

- a fixed response schema (`user_query`, `reasoning`, `tool_calls`, `answer`),
- recording every tool invocation in `tool_calls` with input, output, and success flag,
- validating paths and expressions before processing.

This makes it clear how data is transformed from free-text request to structured, auditable output suitable for later API or UI integration.

## Step 4 - Final submission (22.05)

### Final system description and goal

**Smart Agent System** is a completed Python CLI assistant that solves practical user tasks through a multi-agent workflow with explicit tool use. Compared to the initial plan (Step 1), the system is now fully implemented: it accepts natural-language `--query` input, routes requests automatically, invokes tools during execution, and returns meaningful structured JSON output.

**Goal (achieved):** Provide one reliable interface for arithmetic, local file inspection, and project knowledge lookup, while keeping the architecture transparent (planning, execution, and response layers remain separate and testable).

**Problem solved:** Users no longer need to switch manually between a calculator, file commands, and documentation search. The assistant selects the correct capability and documents every tool call in the response.

**Expected outcome (met):** A working local agent with stable schema output, reproducible tests, install/run instructions, and a clear path for future extension (API, Docker, CI).

### Final explanation of programming concepts and usage

The project evolved from planned concepts (Step 1) to applied engineering patterns (Step 2) and verified behavior (Step 3). Final usage summary:

| Concept | Final role in this project |
|---------|---------------------------|
| Modular packages (`agent`, `models`, `tools`, `main`) | Keeps responsibilities isolated and supports incremental testing |
| Multi-agent workflow | `PlannerAgent` + `ExecutorAgent` + `SmartAssistant` implement divide-and-conquer agent logic |
| Dataclasses (`ToolCall`, `AgentResponse`, `ExecutionContext`) | Enforce consistent machine-readable responses |
| Intent parsing (regex/heuristics) | Converts free text into normalized actions and parameters |
| Safe `ast` evaluation | Prevents unsafe calculator execution |
| `pathlib` + UTF-8 I/O | Reliable local file access with validation |
| Exception handling | Tool-level validation + assistant-level graceful failure responses |
| `argparse` CLI + JSON output | Simple user interface with integration-ready output |
| `pytest` | Continuous verification during development |

**Conclusion:** The final system demonstrates that agent-style software can be built without external LLM APIs when reasoning, routing, and tool invocation are explicit and testable.

### Final description of tools and their role

| Tool | Role in the system | When it is used |
|------|-------------------|-----------------|
| **CalculatorTool** | Computes numeric expressions safely | Math-like queries and explicit calculate requests |
| **FileReaderTool** | Reads and previews local text files | `read file ...` requests |
| **KeywordSearchTool** | Retrieves relevant knowledge-base lines | General questions not classified as math or file read |

**Integration (final state):** `ExecutorAgent` owns tool instances and maps actions to tool calls. `SmartAssistant` records each invocation in `tool_calls` and formats the final `answer`. `main.py` connects the workflow to end users via CLI.

**Extensibility:** New capabilities can be added by implementing a tool class and extending planner/executor routing — without rewriting the orchestration layer.

### Final testing results and conclusions

**Final test run:**

```bash
pytest -q
```

**Result:** 10 passed, 0 failed.

**Coverage achieved:**

- Main workflow: math, file read, knowledge search (3 scenarios)
- Individual tools: calculator, file reader, keyword search (3 scenarios)
- Input validation and errors: empty/unsafe expressions, missing files (4 scenarios)
- Integration integrity: planner → executor → structured response

**Conclusions:**

1. The implemented workflow behaves correctly for all primary use cases defined at the start of the project.
2. Separating tool tests from workflow tests made debugging faster and improved confidence before final submission.
3. Automated negative-path tests confirm validation rules and assistant-level error responses.
4. The project meets the task requirement to test meaningfully during implementation, not only at the end.

### Final deployment preparation

The solution is released as a **controlled local CLI deployment**:

| Item | Status |
|------|--------|
| `requirements.txt` | Provided (`pytest` for development/testing) |
| `pyproject.toml` | Package metadata and editable install support |
| `README.md` | Installation, run examples, testing command |
| `data/` | Default knowledge base and sample files |
| Environment variables | Not required in current version |
| Startup | `python -m boma_agent.main --query "..."` |

**How another user runs it:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
python -m boma_agent.main --query "How do I run tests?"
```

Optional: `--knowledge-base path/to/kb.txt` for custom knowledge data.

### Chosen deployment strategy (final)

**Selected strategy:** staged local release as a command-line tool.

1. **Development** — run and test on developer machine (`pytest`, sample queries).
2. **Controlled test environment** — install on a second machine using README instructions to confirm portability.
3. **Production-like local use** — distribute repository; users install dependencies and run CLI with project data files.

**Why this strategy fits:** The system is deterministic, lightweight, and easy to validate without cloud infrastructure. It minimizes deployment risk while still satisfying “another user can run it in a controlled way.”

**Proposed next steps (not required now, but realistic):**

- add CI (run `pytest` on every push),
- wrap `SmartAssistant` as a REST API for multi-user access,
- containerize with Docker for consistent environments.

### Final project status

From planning (Step 1) to implementation (Step 2), testing and run readiness (Step 3), and this final consolidation (Step 4), the repository now contains a complete agent-based Python solution with documentation, tests, version history on GitHub, and deployment instructions suitable for final evaluation.
