"""Tests for the HTTP server.

We start a real HTTPServer on an ephemeral port and hit it with urllib.
"""

import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from blog_engine.server import make_handler


@pytest.fixture
def running_server(tmp_path):
    """Write two posts to a temp dir, start the server on a random port."""
    (tmp_path / "one.md").write_text(
        "---\ntitle: First\ndate: 2026-09-15\n---\n\n# First\n\nHello one."
    )
    (tmp_path / "two.md").write_text(
        "---\ntitle: Second\ndate: 2026-09-20\n---\n\n# Second\n\nHello two."
    )

    handler = make_handler(str(tmp_path))
    server = HTTPServer(("127.0.0.1", 0), handler)
    server.posts_dir = str(tmp_path)
    host, port = server.server_address

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://{host}:{port}"

    server.shutdown()
    server.server_close()


def _get(url):
    with urllib.request.urlopen(url, timeout=3) as resp:
        return resp.status, resp.read().decode("utf-8")


def test_health_endpoint(running_server):
    status, body = _get(f"{running_server}/health")
    assert status == 200
    assert "ok" in body


def test_index_lists_posts(running_server):
    status, body = _get(f"{running_server}/")
    assert status == 200
    assert "First" in body
    assert "Second" in body


def test_index_sorted_newest_first(running_server):
    _, body = _get(f"{running_server}/")
    # Second (2026-09-20) should appear before First (2026-09-15)
    assert body.index("Second") < body.index("First")


def test_post_page_renders(running_server):
    status, body = _get(f"{running_server}/posts/first")
    assert status == 200
    assert "<h1>First</h1>" in body
    assert "Hello one." in body


def test_post_not_found(running_server):
    with pytest.raises(urllib.error.HTTPError) as exc:
        _get(f"{running_server}/posts/nope")
    assert exc.value.code == 404


def test_unknown_path_returns_404(running_server):
    with pytest.raises(urllib.error.HTTPError) as exc:
        _get(f"{running_server}/whatever")
    assert exc.value.code == 404
