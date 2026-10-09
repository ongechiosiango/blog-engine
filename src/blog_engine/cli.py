"""Command-line entry point for blog-engine."""

from __future__ import annotations

import argparse
import sys
from http.server import HTTPServer
from pathlib import Path

from . import __version__
from .loader import PostError, load_posts
from .server import make_handler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blog-engine",
        description="A tiny HTTP server that serves a Markdown blog.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--posts", default="posts", help="Posts directory (default: posts)")
    parser.add_argument("--version", action="version", version=f"blog-engine {__version__}")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    posts_dir = Path(args.posts)
    if not posts_dir.is_dir():
        print(f"Error: posts directory not found: {args.posts}", file=sys.stderr)
        return 1

    # Fail fast if any post is malformed — better than crashing on first request.
    try:
        posts = load_posts(str(posts_dir))
    except PostError as exc:
        print(f"Error loading posts: {exc}", file=sys.stderr)
        return 1

    handler = make_handler(str(posts_dir))
    server = HTTPServer((args.host, args.port), handler)
    server.posts_dir = str(posts_dir)

    print(f"blog-engine {__version__} listening on http://{args.host}:{args.port}")
    print(f"Loaded {len(posts)} post(s) from {posts_dir}/")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        return 0
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
