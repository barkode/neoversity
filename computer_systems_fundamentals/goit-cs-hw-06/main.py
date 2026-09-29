"""
main.py — Entry point for the web application.

Starts two servers in separate processes:
  - HTTP server on port 3000 (handles routing, static files, form submission)
  - UDP Socket server on port 5000 (receives form data and stores it in MongoDB)
"""

import mimetypes
import os
import socket
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process

from pymongo import MongoClient

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
HTTP_PORT = 3000
SOCKET_PORT = 5000
SOCKET_HOST = "0.0.0.0"

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = "messages_db"
MONGO_COLLECTION = "messages"

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


# ---------------------------------------------------------------------------
# Helper: send a file as an HTTP response
# ---------------------------------------------------------------------------
def send_file(handler: "HttpHandler", file_path: str, status: int = 200) -> None:
    """Read *file_path* from disk and write it as an HTTP response."""
    with open(file_path, "rb") as fh:
        content = fh.read()

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    handler.send_response(status)
    handler.send_header("Content-Type", mime_type)
    handler.send_header("Content-Length", str(len(content)))
    handler.end_headers()
    handler.wfile.write(content)


def send_error_404(handler: "HttpHandler") -> None:
    """Return the custom 404 error page."""
    error_page = os.path.join(TEMPLATES_DIR, "error.html")
    send_file(handler, error_page, status=404)


# ---------------------------------------------------------------------------
# HTTP request handler
# ---------------------------------------------------------------------------
class HttpHandler(BaseHTTPRequestHandler):
    """Handle GET and POST requests for the web application."""

    # --- GET --------------------------------------------------------------- #
    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Route: home page
        if path in ("/", "/index.html"):
            send_file(self, os.path.join(TEMPLATES_DIR, "index.html"))

        # Route: message page
        elif path == "/message.html":
            send_file(self, os.path.join(TEMPLATES_DIR, "message.html"))

        # Static assets: CSS and PNG
        elif path in ("/style.css", "/logo.png"):
            static_file = os.path.join(STATIC_DIR, path.lstrip("/"))
            if os.path.isfile(static_file):
                send_file(self, static_file)
            else:
                send_error_404(self)

        # Anything else → 404
        else:
            send_error_404(self)

    # --- POST -------------------------------------------------------------- #
    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Route: form submission from message.html
        if path == "/message":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)

            # Forward the raw form data to the UDP socket server
            self._forward_to_socket(raw_body)

            # Redirect back to the home page after successful submission
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        else:
            send_error_404(self)

    # --- Internal helpers -------------------------------------------------- #
    def _forward_to_socket(self, data: bytes) -> None:
        """Send *data* to the UDP socket server for processing."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(data, (SOCKET_HOST, SOCKET_PORT))

    def log_message(self, fmt: str, *args) -> None:  # noqa: D102
        """Override to produce cleaner console output."""
        print(f"[HTTP] {self.address_string()} - {fmt % args}")


# ---------------------------------------------------------------------------
# UDP Socket server — receives form data and saves to MongoDB
# ---------------------------------------------------------------------------
def run_socket_server() -> None:
    """
    Listen for UDP datagrams on SOCKET_PORT.

    Each datagram is expected to be a URL-encoded form body such as:
        username=krabaton&message=Hello

    The parsed fields are stored in MongoDB together with the current timestamp.
    """
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((SOCKET_HOST, SOCKET_PORT))
        print(f"[Socket] UDP server listening on {SOCKET_HOST}:{SOCKET_PORT}")

        while True:
            data, addr = sock.recvfrom(4096)
            print(f"[Socket] Received {len(data)} bytes from {addr}")

            try:
                # Decode URL-encoded form data into a dict
                decoded = data.decode("utf-8")
                params = urllib.parse.parse_qs(decoded)

                username = params.get("username", [""])[0]
                message = params.get("message", [""])[0]

                # Build the document and persist it
                document = {
                    "date": str(datetime.now()),
                    "username": username,
                    "message": message,
                }
                collection.insert_one(document)
                print(f"[Socket] Saved to MongoDB: {document}")

            except Exception as exc:  # noqa: BLE001
                print(f"[Socket] Error processing message: {exc}")


# ---------------------------------------------------------------------------
# HTTP server runner
# ---------------------------------------------------------------------------
def run_http_server() -> None:
    """Start the HTTP server and block until interrupted."""
    server = HTTPServer(("0.0.0.0", HTTP_PORT), HttpHandler)
    print(f"[HTTP] Server started on http://0.0.0.0:{HTTP_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[HTTP] Shutting down.")
        server.server_close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Launch the UDP socket server in a separate process
    socket_process = Process(target=run_socket_server, name="socket-server")
    socket_process.start()
    print("[Main] Socket server process started.")

    # Run the HTTP server in the main process
    run_http_server()

    # Clean up if HTTP server exits
    socket_process.terminate()
    socket_process.join()
    print("[Main] All processes stopped.")
