# Blog Engine

[![CI](https://github.com/ongechiosiango/blog-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/ongechiosiango/blog-engine/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A tiny HTTP server that serves a Markdown blog.

## What this is

A ~300-line Python blog engine that reads Markdown files with simple
frontmatter and serves them as an HTML site. It demonstrates:

- HTTP request handling with `http.server`
- Rendering Markdown to HTML with the `markdown` library
- A small frontmatter parser (no YAML dependency)
- Testable server code via a handler factory

## Quick start

    python3 -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"

    blog-engine --port 8000 --posts ./posts

Open http://localhost:8000/ in a browser.

## Post format

    ---
    title: Hello, World
    date: 2026-09-15
    ---

    # Hello, World

    Body markdown goes here.

## Routes

| Route | Response |
|-------|----------|
| GET / | Index of posts, newest first |
| GET /posts/&lt;slug&gt; | A single rendered post |
| GET /health | JSON health check |
| anything else | 404 page |

See docs/usage.md for full details.

## Development

    pip install -e ".[dev]"
    pytest -v

## Contributing

See CONTRIBUTING.md.

## License

MIT - see LICENSE.
