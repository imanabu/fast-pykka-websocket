# FastAPI + Pykka: A WebSocket Demonstration

This project demonstrates how to effectively integrate [FastAPI](https://fastapi.tiangolo.com/) with [Pykka](https://www.pykka.org/) to manage WebSocket connections. It provides a clear, working example of how to handle communication between FastAPI's asynchronous environment and Pykka's thread-based actor model.

## The Goal: Simple, Concurrent WebSockets

Imagine building a real-time application, like a chat room or a live notification system. You need to manage a separate, persistent WebSocket connection for every user. The **Actor Model** is a programming pattern that makes this easy. 

Think of an "Actor" as a specialized worker with its own memory and tasks. You can create one actor for each WebSocket connection, keeping the logic for each user isolated and easy to manage. This avoids many of the complex problems that come with traditional multi-threaded programming.

Pykka is a Python library that brings the Actor Model to your projects.

## The Challenge: Bridging Two Worlds

The main challenge this demo solves is getting FastAPI and Pykka to talk to each other. 

- **FastAPI** is built on `asyncio`, a modern way to handle many network connections at once in a single thread.
- **Pykka Actors** run in their own separate, traditional threads.

Sending messages between FastAPI's `asyncio` world and a Pykka actor's thread world can be tricky. This project shows how to do it correctly, providing a reliable pattern for building robust, real-time applications.

## How to Run This Project

This project uses `uv` for package and environment management. `uv` is a fast, modern replacement for `pip` and `venv`.

1.  **Install `uv`** (if you don't have it):
    - Follow the official installation instructions: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

2.  **Set up the virtual environment and install dependencies:**

    *   **Windows (PowerShell):**
        ```powershell
        uv venv
        . .\.venv\Scripts\activate
        uv pip install -e .
        ```

    *   **macOS / Linux (Bash):**
        ```bash
        uv venv
        source .venv/bin/activate
        uv pip install -e .
        ```

3.  **Start the application:**
    ```bash
    uvicorn main:app --reload
    ```

    Optionally, the Visual Studio Code workspace file contains a debug run
    configuration so you can launch it with a debugger.

4.  **Open the Demo:**
    - Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

## Project Structure

```
fast-pykka-websocket/
├── lib/                  # Main application source code
│   ├── __init__.py
│   ├── actors.py         # Defines the Pykka Actor for WebSocket connections
│   ├── api.py            # Contains the FastAPI endpoints and WebSocket logic
│   └── utils.py          # Utility functions (if any)
├── tests/                # Automated tests
│   ├── __init__.py
│   └── test_WebSockets.py
├── .venv/                # The virtual environment directory (created by `uv`)
├── main.py               # The main entry point to start the application
├── index.html            # The frontend for the demo
├── README.md             # This file
├── pyproject.toml        # Project configuration and dependencies
└── .gitignore
```

