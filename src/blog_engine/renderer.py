"""Convert Markdown text to HTML."""

from __future__ import annotations

import markdown as md


def render_markdown(text: str) -> str:
    """Convert Markdown to HTML using the 'markdown' library."""
    return md.markdown(
        text,
        extensions=["fenced_code", "tables", "sane_lists"],
        output_format="html5",
    )
