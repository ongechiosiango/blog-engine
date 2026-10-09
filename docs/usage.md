# Usage Guide

## Start the server

    blog-engine --port 8000 --posts ./posts

Options:

| Flag | Default | Description |
|------|---------|-------------|
| --host | 127.0.0.1 | Bind address |
| --port, -p | 8000 | Listen port |
| --posts | posts | Directory containing .md posts |
| --version | | Print version and exit |

## Post format

Each post is a `.md` file with simple `key: value` frontmatter:

    ---
    title: Hello, World
    date: 2026-09-15
    ---

    # Hello, World

    Body markdown goes here.

Required fields: `title`, `date` (YYYY-MM-DD).
Optional: `slug` (auto-derived from title if omitted).

## Routes

| Route | Response |
|-------|----------|
| GET / | Index listing all posts, newest first |
| GET /posts/&lt;slug&gt; | A single post rendered to HTML |
| GET /health | `{"status":"ok"}` |
| anything else | 404 page |

## Browser

Open http://localhost:8000/ and click a post.

## Exit codes

- 0 - clean shutdown
- 1 - posts directory missing, or a post failed to parse
