"""Tests for the frontmatter parser."""

import pytest

from blog_engine.frontmatter import FrontmatterError, split_frontmatter


def test_no_frontmatter():
    text = "# Just a heading\n\nBody."
    meta, body = split_frontmatter(text)
    assert meta == {}
    assert body == text


def test_simple_frontmatter():
    text = "---\ntitle: Hi\ndate: 2026-10-02\n---\n\nBody here."
    meta, body = split_frontmatter(text)
    assert meta["title"] == "Hi"
    assert meta["date"] == "2026-10-02"
    assert body.strip() == "Body here."


def test_unclosed_frontmatter():
    text = "---\ntitle: Hi\nbody without closing"
    with pytest.raises(FrontmatterError, match="never closed"):
        split_frontmatter(text)


def test_bad_line_in_frontmatter():
    text = "---\ntitle Hi\n---\nBody."
    with pytest.raises(FrontmatterError, match="Bad frontmatter"):
        split_frontmatter(text)


def test_comments_ignored():
    text = "---\n# a comment\ntitle: X\n---\nBody."
    meta, _ = split_frontmatter(text)
    assert meta == {"title": "X"}
