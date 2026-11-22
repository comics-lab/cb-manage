#!/usr/bin/env python3
"""Verify CB-MANAGE governance references and basic semantic fit."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_SOURCES = [
    ROOT / "AGENTS.md", ROOT / "AGENTS-master.md",
    ROOT / "docs/agents/system/registry/Agent_System_Index.md",
    ROOT / "docs/agents/system/registry/Agent_Registry.md",
    ROOT / "docs/agents/system/registry/Director_Routing_Matrix.md",
]
PATH_PREFIXES = ("AGENTS", "docs/", "truth/", "skills/", ".agents/", "scripts/", "config/", ".github/", "logs/", "README.md")


def candidates(text: str) -> list[str]:
    found: list[str] = []
    for match in re.findall(r"`([^`]+)`|#include\s+([^\s]+)", text):
        value = next((part for part in match if part), "").rstrip(".,;:)")
        if not value or any(token in value for token in ("YYYY", "<", ">", "*")):
            continue
        if value.startswith(PATH_PREFIXES) or value.startswith(("./", "../")):
            if not value.endswith("/"):
                found.append(value)
    return found


def resolve(source: Path, candidate: str) -> Path | None:
    path = (source.parent / candidate if candidate.startswith(("./", "../")) else ROOT / candidate).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError:
        return None
    return path


def main() -> int:
    queue = [path for path in REFERENCE_SOURCES if path.is_file()]
    visited: set[Path] = set()
    missing: list[str] = []
    semantic: list[str] = []
    checked = 0
    while queue:
        source = queue.pop(0).resolve()
        if source in visited or not source.is_file():
            continue
        visited.add(source)
        for candidate in candidates(source.read_text(encoding="utf-8")):
            path = resolve(source, candidate)
            if path is None:
                continue
            checked += 1
            if not path.is_file():
                missing.append(f"{source.relative_to(ROOT)} -> {path.relative_to(ROOT)}")
                continue
            if path.suffix.lower() in {".md", ".yaml", ".yml", ".txt"}:
                queue.append(path)
            text = path.read_text(encoding="utf-8")
            lower = text.lower()
            relative = path.relative_to(ROOT).as_posix()
            if relative.endswith("Agent_System_Index.md") and "index" not in lower[:500]:
                semantic.append(f"{relative}: missing index identity")
            if relative.endswith("Agent_Registry.md") and "registry" not in lower[:500]:
                semantic.append(f"{relative}: missing registry identity")
            if relative.endswith("Director_Routing_Matrix.md") and "routing" not in lower[:700]:
                semantic.append(f"{relative}: missing routing identity")
            if relative.startswith(".agents/skills/") and relative.endswith("/SKILL.md"):
                if not re.search(r"^name:\s*\S+", text, re.MULTILINE):
                    semantic.append(f"{relative}: missing name frontmatter")
                if not re.search(r"^description:\s*\S+", text, re.MULTILINE):
                    semantic.append(f"{relative}: missing description frontmatter")
    print(f"Checked {checked} governance references.")
    if missing or semantic:
        if missing:
            print("MISSING:\n" + "\n".join(f"- {item}" for item in sorted(set(missing))))
        if semantic:
            print("SEMANTIC WARNINGS:\n" + "\n".join(f"- {item}" for item in sorted(set(semantic))))
        return 1
    print("All governance references exist and pass basic semantic checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
