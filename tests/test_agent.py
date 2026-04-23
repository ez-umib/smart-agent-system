from pathlib import Path

from boma_agent import BomaAssistant


def test_agent_math_flow() -> None:
    agent = BomaAssistant()
    result = agent.run("4 + 5 * 2")
    assert result.tool_calls
    assert result.tool_calls[0].tool_name == "calculator"
    assert "14.0" in result.answer


def test_agent_file_flow(tmp_path: Path) -> None:
    file_path = tmp_path / "note.txt"
    file_path.write_text("alpha beta", encoding="utf-8")
    agent = BomaAssistant()
    result = agent.run(f"read file {file_path}")
    assert result.tool_calls[0].tool_name == "file_reader"
    assert "alpha beta" in result.answer


def test_agent_knowledge_flow(tmp_path: Path) -> None:
    kb_path = tmp_path / "kb.txt"
    kb_path.write_text(
        "Python supports pytest.\n"
        "Agents can call tools.\n",
        encoding="utf-8",
    )
    agent = BomaAssistant(knowledge_base_path=str(kb_path))
    result = agent.run("How do I test with pytest?")
    assert result.tool_calls[0].tool_name == "keyword_search"
    assert "pytest" in result.answer.lower()
