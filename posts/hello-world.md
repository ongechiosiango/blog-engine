---
title: Hello, World
date: 2026-09-15
---

# Hello, World

Welcome to my blog, served by a ~150-line Python HTTP server.

## Why?

Because I wanted to understand how a blog engine works under the hood:

- **Reading posts** from a directory of Markdown files
- **Rendering** them to HTML with the `markdown` library
- **Serving** them over HTTP with `http.server`

## Code sample

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

That's it. Simple is good.
