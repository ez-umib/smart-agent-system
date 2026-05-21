import pytest
from pathlib import Path

from boma_agent.tools.calculator import CalculatorTool
from boma_agent.tools.file_reader import FileReaderTool
from boma_agent.tools.keyword_search import KeywordSearchTool


def test_calculator_basic_expression() -> None:
    tool = CalculatorTool()
    assert tool.run("2 + 3 * 4") == "14.0"


def test_file_reader_reads_content(tmp_path: Path) -> None:
    file_path = tmp_path / "input.txt"
    file_path.write_text("hello world", encoding="utf-8")
    tool = FileReaderTool()
    assert tool.run(str(file_path)) == "hello world"


def test_keyword_search_returns_matching_lines(tmp_path: Path) -> None:
    corpus = tmp_path / "kb.txt"
    corpus.write_text(
        "Use pytest for testing.\n"
        "Use virtualenv for environments.\n"
        "Deployment can be local.\n",
        encoding="utf-8",
    )
    tool = KeywordSearchTool()
    result = tool.run("testing with pytest", str(corpus))
    assert "pytest" in result.lower()


def test_calculator_rejects_empty_expression() -> None:
    tool = CalculatorTool()
    with pytest.raises(ValueError, match="cannot be empty"):
        tool.run("   ")


def test_calculator_rejects_unsafe_expression() -> None:
    tool = CalculatorTool()
    with pytest.raises(ValueError, match="Unsupported expression node"):
        tool.run("__import__('os').system('echo')")


def test_file_reader_rejects_missing_file() -> None:
    tool = FileReaderTool()
    with pytest.raises(FileNotFoundError):
        tool.run("/tmp/does-not-exist-smart-agent.txt")
