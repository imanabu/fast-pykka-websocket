# Demonstration of WebSocket Implementation with Pyakka, FastAPI and clusans

## Why Is This Demo?

Pyakka's Actor Model allows us to develop multi-threaded Python applications
in a more manageable and thread-safe manner.

However, when we integrate FastAPI, inter-thread messaging becomes challenging
because messages must cross event-loop boundaries between 
the FastAPI server (which hosts the WebSockets) and the PyAkka actors. 

Getting this to work correctly requires familiarity with the `asyncio` package.

This StackOverflow discussion shows this type of issue https://stackoverflow.com/questions/32889527/is-there-a-way-to-use-asyncio-queue-in-multiple-threads

## Setting Up

This project uses `uv`. If you are not yet familiar with it, it is a better
`pip` Please ask your code assist to help you install it.

#### Windows 
```powershell
uv venv
. .\.venv\Scripts\activate.ps
```

#### Mac and Linux
```bash
uv venv
. .\bin\activate
```

## Project Structure

```
fast-pyakka-websocket/
├── lib/         # Main application package
│   ├── __init__.py
│   ├── actors.py          # PyAkka actor definitions
│   ├── api.py             # FastAPI Logic
│   └── utils.py           # Utility functions
├── tests/                 # Test suite
│   ├── __init__.py
│   └── test_WebSockets.py
├── .venv/                 # Virtual environment (not committed)
├── main.py                 # Virtual environment (not committed)
├── README.md
├── pyproject.toml         # Project metadata and dependencies
└── .gitignore
```

