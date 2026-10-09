"""Parse simple YAML-ish frontmatter from Markdown posts.

We only support the subset we need:

    ---
    title: Hello, World
    date: 2026-09-15
    ---

    body markdown goes here

No nested structures, no lists, no quoting rules. Just key: value.
"""

from __future__ import annotations


class FrontmatterError(Exception):
    """Raised when frontmatter is malformed."""


def split_frontmatter(text: str) -> tuple:
    """Return (metadata_dict, body_markdown)."""
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    if lines[0].strip() != "---":
        return {}, text

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise FrontmatterError("Frontmatter opened with '---' but never closed.")

    meta = {}
    for line in lines[1:end_idx]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise FrontmatterError(f"Bad frontmatter line: {line!r}")
        key, _, value = stripped.partition(":")
        meta[key.strip()] = value.strip()

    body = "\n".join(lines[end_idx + 1:]).lstrip("\n")
    return meta, body
