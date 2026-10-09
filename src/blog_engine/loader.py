"""Load posts from a directory of Markdown files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from .frontmatter import FrontmatterError, split_frontmatter


class PostError(Exception):
    """Raised when a post file is malformed."""


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    text = text.lower().strip()
    return _SLUG_RE.sub("-", text).strip("-") or "post"


@dataclass
class Post:
    slug: str
    title: str
    date: date
    body_markdown: str

    @property
    def iso_date(self) -> str:
        return self.date.isoformat()


def load_post(path: Path) -> Post:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PostError(f"Could not read {path}: {exc}") from exc

    try:
        meta, body = split_frontmatter(text)
    except FrontmatterError as exc:
        raise PostError(f"{path}: {exc}") from exc

    title = meta.get("title")
    if not title:
        raise PostError(f"{path}: missing 'title' in frontmatter.")

    raw_date = meta.get("date")
    if not raw_date:
        raise PostError(f"{path}: missing 'date' in frontmatter.")
    try:
        parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except ValueError as exc:
        raise PostError(f"{path}: 'date' must be YYYY-MM-DD, got {raw_date!r}") from exc

    slug = meta.get("slug") or slugify(title)

    return Post(slug=slug, title=title, date=parsed_date, body_markdown=body)


def load_posts(posts_dir: str) -> list:
    """Load every .md file in a directory, sorted newest first."""
    p = Path(posts_dir)
    if not p.exists():
        raise PostError(f"Posts directory not found: {posts_dir}")
    if not p.is_dir():
        raise PostError(f"Not a directory: {posts_dir}")

    posts = []
    for md_file in sorted(p.glob("*.md")):
        posts.append(load_post(md_file))

    posts.sort(key=lambda post: post.date, reverse=True)
    return posts


def find_post(posts_dir: str, slug: str):
    """Return the Post with the given slug, or None."""
    for post in load_posts(posts_dir):
        if post.slug == slug:
            return post
    return None
