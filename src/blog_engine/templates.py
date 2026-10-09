"""Minimal inline HTML templates. No Jinja2 needed."""

from __future__ import annotations

BASE_HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      max-width: 720px; margin: 2rem auto; padding: 0 1rem;
      color: #222; background: #fff; line-height: 1.65;
    }
    a { color: #0066cc; }
    h1, h2, h3 { line-height: 1.25; }
    pre, code {
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      background: #f4f4f4; border-radius: 4px;
    }
    code { padding: 0.15em 0.35em; }
    pre { padding: 0.9em 1em; overflow-x: auto; }
    pre code { padding: 0; background: transparent; }
    .post-meta { color: #666; font-size: 0.9em; }
    .post-list { list-style: none; padding: 0; }
    .post-list li { padding: 0.8rem 0; border-bottom: 1px solid #eee; }
    header { border-bottom: 1px solid #eee; padding-bottom: 1rem; margin-bottom: 2rem; }
    header a { color: #222; text-decoration: none; font-weight: bold; font-size: 1.25rem; }
    @media (prefers-color-scheme: dark) {
      body { color: #e6e6e6; background: #121212; }
      a { color: #6cb6ff; }
      header a { color: #e6e6e6; }
      pre, code { background: #1e1e1e; }
      header, .post-list li { border-color: #2a2a2a; }
      .post-meta { color: #999; }
    }
  </style>
</head>
<body>
  <header><a href="/">My Blog</a></header>
"""

BASE_TAIL = """
</body>
</html>
"""


def _head(title: str) -> str:
    return BASE_HEAD_TEMPLATE.replace("__TITLE__", _escape(title))


def index_page(posts) -> str:
    parts = [_head("My Blog"), "<h1>Posts</h1>"]
    if not posts:
        parts.append("<p>No posts yet.</p>")
    else:
        parts.append('<ul class="post-list">')
        for post in posts:
            parts.append(
                f'<li><a href="/posts/{post.slug}">{_escape(post.title)}</a>'
                f'<div class="post-meta">{post.iso_date}</div></li>'
            )
        parts.append("</ul>")
    parts.append(BASE_TAIL)
    return "".join(parts)


def post_page(post, body_html: str) -> str:
    return "".join([
        _head(post.title),
        f"<article><h1>{_escape(post.title)}</h1>",
        f'<p class="post-meta">{post.iso_date}</p>',
        body_html,
        '</article><p><a href="/">&larr; All posts</a></p>',
        BASE_TAIL,
    ])


def not_found_page() -> str:
    return _head("404") + "<h1>404</h1><p>Not found.</p>" + BASE_TAIL


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )
