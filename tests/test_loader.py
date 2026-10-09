"""Tests for the post loader."""

import pytest

from blog_engine.loader import PostError, find_post, load_post, load_posts, slugify


def _write(tmp_path, name, content):
    p = tmp_path / name
    p.write_text(content)
    return p


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("   Weird   Spaces  ") == "weird-spaces"
    assert slugify("") == "post"


def test_load_post_from_file(tmp_path):
    p = _write(tmp_path, "a.md", "---\ntitle: Hello\ndate: 2026-10-02\n---\nBody.")
    post = load_post(p)
    assert post.title == "Hello"
    assert post.slug == "hello"
    assert post.date.year == 2026
    assert post.body_markdown.strip() == "Body."


def test_load_post_missing_title(tmp_path):
    p = _write(tmp_path, "a.md", "---\ndate: 2026-10-02\n---\nBody.")
    with pytest.raises(PostError, match="title"):
        load_post(p)


def test_load_post_missing_date(tmp_path):
    p = _write(tmp_path, "a.md", "---\ntitle: X\n---\nBody.")
    with pytest.raises(PostError, match="date"):
        load_post(p)


def test_load_post_bad_date(tmp_path):
    p = _write(tmp_path, "a.md", "---\ntitle: X\ndate: not-a-date\n---\nBody.")
    with pytest.raises(PostError, match="YYYY-MM-DD"):
        load_post(p)


def test_load_posts_sorted_newest_first(tmp_path):
    _write(tmp_path, "old.md", "---\ntitle: Old\ndate: 2026-01-01\n---\n.")
    _write(tmp_path, "new.md", "---\ntitle: New\ndate: 2026-06-01\n---\n.")
    posts = load_posts(str(tmp_path))
    assert [p.title for p in posts] == ["New", "Old"]


def test_load_posts_missing_dir(tmp_path):
    with pytest.raises(PostError, match="not found"):
        load_posts(str(tmp_path / "nope"))


def test_find_post(tmp_path):
    _write(tmp_path, "a.md", "---\ntitle: Hello World\ndate: 2026-10-02\n---\nBody.")
    post = find_post(str(tmp_path), "hello-world")
    assert post is not None
    assert post.title == "Hello World"


def test_find_post_missing(tmp_path):
    _write(tmp_path, "a.md", "---\ntitle: Hello\ndate: 2026-10-02\n---\nBody.")
    assert find_post(str(tmp_path), "nope") is None
