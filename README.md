# PY175: Network Applications with Python

From bytes on the wire to buttons in the browser. This repo follows Launch School’s PY175 journey, starting with raw TCP sockets and finishing with a small Flask web app that serves HTML, JSON, and a tiny UI.

---

## Contents

- `src/sockets/` raw TCP client and server examples
- `src/flask_app/` minimal Flask project with routes, templates, static assets
- `tests/` simple pytest checks
- `requirements.txt` runtime dependencies
- `Makefile` quick commands for setup and running
- `.env.example` sample environment vars
- `README.md` you are here

~~~text
.
├── src
│   ├── sockets
│   │   ├── tcp_client.py
│   │   └── tcp_server.py
│   └── flask_app
│       ├── app.py
│       ├── templates
│       │   └── index.html
│       └── static
│           └── styles.css
├── tests
│   └── test_smoke.py
├── requirements.txt
├── Makefile
└── README.md
~~~

---

## Quick Start

### 1. Setup

~~~bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
~~~

### 2. Run the TCP server and client

In one terminal:
~~~bash
python src/sockets/tcp_server.py
~~~

In a second terminal:
~~~bash
python src/sockets/tcp_client.py
~~~

### 3. Run the Flask app

~~~bash
export FLASK_APP=src/flask_app/app.py
flask run --port 8080
~~~

Visit `http://localhost:8080`

**Cloud9 note**: use ports 8080–8083. Use the Run button to launch a server, then open with the Browser button.

---

## Lessons and Milestones

1) **Opening a TCP connection with `socket`**
   - Create a server socket, bind to host and port, accept a client
   - Create a client socket, connect, send, receive, close
   - Parse a minimal HTTP request line by hand for learning value

2) **Flask basics, build a tiny web design**
   - App basics, routes, request and response
   - Jinja2 templates, static files, simple HTML and CSS
   - JSON endpoints for front end fetch calls

3) **Routing and parameters**
   - Path and query params, form handling
   - Return JSON for small AJAX interactions

4) **State lite**
   - Sessions and cookies for a simple “remember me” feel
   - Flash messages, basic config and secrets

5) **Project structure and local deployment**
   - Blueprints for growth, environment configs
   - Running on a chosen port and handling reload

6) **Testing, quality, and dev flow**
   - pytest smoke tests, black formatting, ruff linting
   - Makefile targets for repeatable commands

---

## Code Snacks

### Minimal TCP server

~~~python
# src/sockets/tcp_server.py
import socket

HOST = "127.0.0.1"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024) or b""
            print(f"From {addr} got {data!r}")
            conn.sendall(b"Hello from TCP server")
~~~

### Minimal TCP client

~~~python
# src/sockets/tcp_client.py
import socket

HOST = "127.0.0.1"
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((HOST, PORT))
    c.sendall(b"Ping")
    print(c.recv(1024).decode())
~~~

### Minimal Flask app

~~~python
# src/flask_app/app.py
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html", title="PY175 Mini App")

@app.get("/api/ping")
def ping():
    who = request.args.get("who", "world")
    return jsonify(message=f"Hello, {who}")

if __name__ == "__main__":
    app.run(port=8080)
~~~

~~~html
<!-- src/flask_app/templates/index.html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }
      main { max-width: 720px; margin: auto; }
      button { padding: .6rem 1rem; border-radius: .5rem; border: 1px solid #ddd; cursor: pointer; }
      pre { background: #f6f8fa; padding: 1rem; border-radius: .5rem; }
    </style>
  </head>
  <body>
    <main>
      <h1>PY175 Mini App</h1>
      <button id="ping">Ping API</button>
      <pre id="out">Click the button to call /api/ping</pre>
    </main>
    <script>
      document.getElementById("ping").onclick = async () => {
        const res = await fetch("/api/ping?who=PY175");
        const json = await res.json();
        document.getElementById("out").textContent = JSON.stringify(json, null, 2);
      };
    </script>
  </body>
</html>
~~~

---

## Makefile

~~~makefile
setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

run-server:
\tpython src/sockets/tcp_server.py

run-client:
\tpython src/sockets/tcp_client.py

run-flask:
\tFLASK_APP=src/flask_app/app.py flask run --port 8080

test:
\tpytest -q

fmt:
\tblack src tests
\truff check src tests --fix
~~~

---

## Requirements

~~~text
flask
pytest
black
ruff
~~~

---

## Goals

- Understand sockets, TCP flow, request and response basics
- Build a small Flask app with routes, templates, and JSON
- Practice clean structure, tests, and repeatable commands

---

## Contributing

Fork, branch, commit in small slices. Open a pull request with a clear summary and steps to verify.

---

## License

MIT
