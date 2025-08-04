import uvicorn
from lib.api import app  # Adjust the import path as necessary

if __name__ == "__main__":
    # Start the FastAPI application
    # Note the WS flags added here
    uvicorn.run(app, host="127.0.0.1",
                ws="auto",
                ws_ping_interval=10,
                ws_ping_timeout=20,
                port=8000)

