from __future__ import annotations

from pathlib import Path


class KeywordSearchTool:
    name = "keyword_search"

    def run(self, query: str, corpus_path: str, top_k: int = 3) -> str:
        text = Path(corpus_path).read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        terms = [term.lower() for term in query.split() if len(term) > 2]
        if not terms:
            return "No searchable keywords found in query."

        scored: list[tuple[int, str]] = []
        for line in lines:
            line_l = line.lower()
            score = sum(1 for term in terms if term in line_l)
            if score > 0:
                scored.append((score, line))

        if not scored:
            return "No relevant entries found."

        scored.sort(key=lambda item: item[0], reverse=True)
        selected = [line for _, line in scored[:top_k]]
        return "\n".join(selected)
