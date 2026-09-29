# Python Web + Socket Application

A simple Python web application that demonstrates HTTP routing, UDP socket
communication, and MongoDB persistence — all packaged with Docker Compose.

---

## Architecture

```
Browser
  │  HTTP GET/POST (port 3000)
  ▼
HTTP Server  (main process, BaseHTTPRequestHandler)
  │  UDP datagram (port 5000)
  ▼
UDP Socket Server  (child process, socket.SOCK_DGRAM)
  │  insert document
  ▼
MongoDB  (Docker service, port 27017)
```

### Ports

| Service         | Port  | Protocol |
|-----------------|-------|----------|
| HTTP web server | 3000  | TCP      |
| Socket server   | 5000  | UDP      |
| MongoDB         | 27017 | TCP      |

---

## Project Structure

```
web_socket_app/
├── main.py             # Single entry point — starts both servers
├── Dockerfile          # Container definition for the Python app
├── docker-compose.yaml # Orchestration: app + MongoDB
├── requirements.txt    # Python dependencies (pymongo)
├── templates/
│   ├── index.html      # Home page
│   ├── message.html    # Message form page
│   └── error.html      # 404 error page
└── static/
    ├── style.css       # Custom stylesheet
    └── logo.png        # Navigation logo
```

---

## How It Works

1. **HTTP Server** (`BaseHTTPRequestHandler`, port 3000):
   - `GET /` or `GET /index.html` → returns `index.html`
   - `GET /message.html` → returns `message.html` with the contact form
   - `GET /style.css`, `GET /logo.png` → serves static assets
   - `POST /message` → reads the URL-encoded form body and forwards it
     to the UDP socket server, then redirects to `/`
   - Any other route → returns `error.html` with HTTP 404

2. **UDP Socket Server** (child process, port 5000):
   - Receives URL-encoded datagrams from the HTTP server
   - Parses `username` and `message` fields
   - Writes a document to MongoDB with the current timestamp:
     ```json
     {
       "date": "2022-10-29 20:20:58.020261",
       "username": "krabaton",
       "message": "First message"
     }
     ```

3. **MongoDB** (Docker service):
   - Database: `messages_db`
   - Collection: `messages`
   - Data is stored in a named Docker volume (`mongo_data`) so it
     persists across container restarts and re-builds.

---

## Running with Docker Compose

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) ≥ 20.10
- [Docker Compose](https://docs.docker.com/compose/install/) ≥ 2.x

### Start

```bash
docker-compose up --build
```

The application will be available at <http://localhost:3000>.

### Stop

```bash
docker-compose down
```

To also remove the MongoDB volume (deletes all stored messages):

```bash
docker-compose down -v
```

---

## Running Locally (without Docker)

### Prerequisites

```bash
pip install pymongo
```

Make sure a MongoDB instance is reachable on `localhost:27017`, or set
the environment variables:

```bash
export MONGO_HOST=localhost
export MONGO_PORT=27017
```

### Start

```bash
cd web_socket_app
python main.py
```

---

## Inspecting Stored Messages

Connect to the running MongoDB container and query the collection:

```bash
docker exec -it mongo_db mongosh
```

Inside the `mongosh` shell:

```js
use messages_db
db.messages.find().pretty()
```

---

## Environment Variables

| Variable     | Default     | Description                    |
|--------------|-------------|--------------------------------|
| `MONGO_HOST` | `localhost` | Hostname of the MongoDB server |
| `MONGO_PORT` | `27017`     | Port of the MongoDB server     |
