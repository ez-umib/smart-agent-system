from __future__ import annotations

from pathlib import Path


class FileReaderTool:
    name = "file_reader"

    def run(self, path: str, max_chars: int = 2000) -> str:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {path}")

        content = file_path.read_text(encoding="utf-8")
        if len(content) <= max_chars:
            return content
        return content[:max_chars] + "\n...[truncated]"
