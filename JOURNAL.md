# Journal

## Step 1 - 24.04

### Planned system and goal

The planned system is a Python command-line assistant named **Boma Agent System**.
Its goal is to receive user requests and solve practical tasks through an agent workflow that uses tools during execution.

### AI / agent-based approach

The architecture uses an agent workflow with separated responsibilities:

- **PlannerAgent** interprets user intent and selects an action.
- **ExecutorAgent** executes the selected action by calling a concrete tool.
- **BomaAssistant** orchestrates planning, execution, error handling, and final response formatting.

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
