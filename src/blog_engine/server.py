"""HTTP request handler that serves the blog."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from .loader import PostError, find_post, load_posts
from .renderer import render_markdown
from .templates import index_page, not_found_page, post_page


def make_handler(posts_dir: str):
    """Return a BaseHTTPRequestHandler subclass bound to a posts directory."""

    class BlogHandler(BaseHTTPRequestHandler):
        server_version = "BlogEngine/0.1.0"

        def do_GET(self):  # noqa: N802  (http.server requires this name)
            path = urlparse(self.path).path

            if path == "/" or path == "":
                self._serve_index()
            elif path == "/health":
                self._serve_json(b'{"status":"ok"}')
            elif path.startswith("/posts/"):
                slug = path[len("/posts/"):].strip("/")
                self._serve_post(slug)
            else:
                self._serve_404()

        # --- individual routes ---

        def _serve_index(self):
            try:
                posts = load_posts(self.server.posts_dir)
            except PostError as exc:
                self._serve_500(str(exc))
                return
            self._send_html(200, index_page(posts))

        def _serve_post(self, slug: str):
            try:
                post = find_post(self.server.posts_dir, slug)
            except PostError as exc:
                self._serve_500(str(exc))
                return
            if post is None:
                self._serve_404()
                return
            body_html = render_markdown(post.body_markdown)
            self._send_html(200, post_page(post, body_html))

        # --- helpers ---

        def _send_html(self, status: int, body: str):
            payload = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _serve_json(self, payload: bytes):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _serve_404(self):
            self._send_html(404, not_found_page())

        def _serve_500(self, message: str):
            self._send_html(500, f"<h1>500</h1><pre>{message}</pre>")

        def log_message(self, fmt, *args):  # noqa: A003
            # Silence default logging; the CLI prints its own line.
            pass

    return BlogHandler
