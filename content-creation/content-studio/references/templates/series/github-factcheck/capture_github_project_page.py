#!/usr/bin/env python3
"""Capture the first viewport of a GitHub repo page for fact-check covers.

This uses Chrome DevTools Protocol with only Python stdlib, avoiding a hard
Playwright dependency inside the skill. The output is intended for
`cover_style: series_github_project` in render_github_factcheck.py.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import shutil
import socket
import struct
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request


DEFAULT_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def find_chrome() -> str:
    candidates = [
        os.environ.get("CHROME_BIN"),
        DEFAULT_CHROME,
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]
    for path in candidates:
        if path and pathlib.Path(path).exists():
            return path
    raise RuntimeError("Chrome not found. Set CHROME_BIN to a Chrome/Chromium executable.")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def http_json(url: str, method: str = "GET", timeout: float = 1.0) -> dict:
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wait_json(url: str, timeout: float = 12.0) -> dict:
    deadline = time.time() + timeout
    last: Exception | None = None
    while time.time() < deadline:
        try:
            return http_json(url)
        except Exception as exc:  # noqa: BLE001 - retry Chrome startup races.
            last = exc
            time.sleep(0.2)
    raise RuntimeError(f"Timed out waiting for {url}: {last}")


class WebSocket:
    def __init__(self, url: str):
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "ws":
            raise RuntimeError(f"Only ws:// CDP endpoints are supported: {url}")
        self.sock = socket.create_connection((parsed.hostname, parsed.port), timeout=8)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(request.encode("ascii"))
        response = self._read_until(b"\r\n\r\n")
        if b" 101 " not in response.split(b"\r\n", 1)[0]:
            raise RuntimeError(f"WebSocket handshake failed: {response[:120]!r}")

    def _read_exact(self, n: int) -> bytes:
        chunks: list[bytes] = []
        remaining = n
        while remaining:
            chunk = self.sock.recv(remaining)
            if not chunk:
                raise RuntimeError("WebSocket closed")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def _read_until(self, marker: bytes) -> bytes:
        data = b""
        while marker not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise RuntimeError("Socket closed during handshake")
            data += chunk
        return data

    def send_json(self, payload: dict) -> None:
        raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        mask = os.urandom(4)
        header = bytearray([0x81])
        if len(raw) < 126:
            header.append(0x80 | len(raw))
        elif len(raw) < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", len(raw)))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", len(raw)))
        masked = bytes(byte ^ mask[i % 4] for i, byte in enumerate(raw))
        self.sock.sendall(bytes(header) + mask + masked)

    def recv_json(self) -> dict:
        while True:
            first, second = self._read_exact(2)
            opcode = first & 0x0F
            masked = bool(second & 0x80)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._read_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._read_exact(8))[0]
            mask = self._read_exact(4) if masked else b""
            payload = self._read_exact(length)
            if masked:
                payload = bytes(byte ^ mask[i % 4] for i, byte in enumerate(payload))
            if opcode == 8:
                raise RuntimeError("WebSocket closed by Chrome")
            if opcode == 1:
                return json.loads(payload.decode("utf-8"))

    def close(self) -> None:
        self.sock.close()


class CDP:
    def __init__(self, ws_url: str):
        self.ws = WebSocket(ws_url)
        self.next_id = 1

    def call(self, method: str, params: dict | None = None, timeout: float = 20.0) -> dict:
        msg_id = self.next_id
        self.next_id += 1
        self.ws.send_json({"id": msg_id, "method": method, "params": params or {}})
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = self.ws.recv_json()
            if msg.get("id") != msg_id:
                continue
            if "error" in msg:
                raise RuntimeError(f"CDP {method} failed: {msg['error']}")
            return msg.get("result", {})
        raise RuntimeError(f"Timed out waiting for CDP response: {method}")

    def close(self) -> None:
        self.ws.close()


def normalize_repo(value: str) -> str:
    value = value.strip()
    if value.startswith("http"):
        path = urllib.parse.urlparse(value).path.strip("/")
        parts = path.split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"
    if "/" not in value:
        raise RuntimeError("Use owner/repo or a GitHub repo URL.")
    return value.strip("/")


def capture(repo: str, out: pathlib.Path, width: int, height: int, settle: float) -> None:
    repo = normalize_repo(repo)
    url = f"https://github.com/{repo}"
    chrome = find_chrome()
    port = free_port()
    out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="github-factcheck-chrome-") as profile:
        proc = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--no-first-run",
                "--disable-extensions",
                "--disable-background-networking",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile}",
                f"--window-size={width},{height}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            wait_json(f"http://127.0.0.1:{port}/json/version")
            target_url = f"http://127.0.0.1:{port}/json/new?{urllib.parse.quote('about:blank', safe=':/')}"
            try:
                target = http_json(target_url, method="PUT", timeout=3)
            except Exception:
                target = http_json(target_url, method="GET", timeout=3)
            cdp = CDP(target["webSocketDebuggerUrl"])
            try:
                cdp.call("Page.enable")
                cdp.call("Runtime.enable")
                cdp.call("Emulation.setDeviceMetricsOverride", {
                    "width": width,
                    "height": height,
                    "deviceScaleFactor": 1,
                    "mobile": False,
                })
                cdp.call("Page.navigate", {"url": url})
                deadline = time.time() + 30
                while time.time() < deadline:
                    state = cdp.call("Runtime.evaluate", {"expression": "document.readyState"})
                    if state.get("result", {}).get("value") == "complete":
                        break
                    time.sleep(0.4)
                time.sleep(settle)
                cdp.call("Runtime.evaluate", {"expression": "window.scrollTo(0, 0)"})
                shot = cdp.call("Page.captureScreenshot", {
                    "format": "png",
                    "fromSurface": True,
                    "captureBeyondViewport": False,
                })
                out.write_bytes(base64.b64decode(shot["data"]))
            finally:
                cdp.close()
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="owner/repo or GitHub repo URL")
    parser.add_argument("--out", required=True, type=pathlib.Path)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=1050)
    parser.add_argument("--settle", type=float, default=5.0, help="extra seconds after load")
    args = parser.parse_args()
    capture(args.repo, args.out, args.width, args.height, args.settle)
    print(f"captured={args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
