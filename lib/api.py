from contextlib import asynccontextmanager
import asyncio
import threading
# import weakref
from typing import Any, Set, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from pykka import ActorRef

from lib.actors import ActorWsMessageSender

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (if any) goes here
    yield
    # Shutdown code - your existing logic goes here
    print("Shutting down, stopping all actors...")
    stop_all_actors()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=".")

# Global registry for active actors - using thread-safe set
active_actors: Set[ActorRef[Any]] = set()
active_actors_lock = threading.Lock()

# Optional: Map websockets to their corresponding actors for easier cleanup
websocket_to_actor: Dict[WebSocket, ActorRef[Any]] = {}
websocket_to_actor_lock = threading.Lock()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Create and start a new actor for this WebSocket connection
    actor_ref = None

    try:
        # Instantiate and start the actor, note that this is how
        # we pass websocket to the __init__ of the actor.
        # We cannot directly instantiate the ActorWsMessageSender.
        actor_ref = ActorWsMessageSender.start(websocket=websocket)

        # Add to global registry (thread-safe)
        with active_actors_lock:
            active_actors.add(actor_ref)

        # Add to websocket mapping (thread-safe)
        with websocket_to_actor_lock:
            websocket_to_actor[websocket] = actor_ref

        print(f"Started actor {actor_ref} for WebSocket connection")
        print(f"Active actors count: {len(active_actors)}")

        # Keep the connection alive and handle disconnection
        while True:
            try:
                # You can receive messages from client here if needed
                try:
                    # IMPORTANT:
                    # Most AI will not provide this crucial line of code!
                    # While our demo does not receive any websocket payload from
                    # the client side, this call is essential.
                    # If we do not do this, this whole loop will be stuck
                    # and the demo will look frozen. 
                    message = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                    # Optionally forward to actor or handle client messages
                    actor_ref.tell(f"Client message: {message}")
                except asyncio.TimeoutError:
                    pass # Timeout is expected, just continue

            except WebSocketDisconnect:
                # print stack trace
                import traceback
                traceback.print_exc()
                
                print("WebSocket disconnected")
                break

    except Exception as e:
        print(f"Error in WebSocket endpoint: {e}")

    finally:
        # Clean up: stop actor and remove from registries
        if actor_ref:
            try:
                # Stop the actor
                actor_ref.stop()
                print(f"Stopped actor {actor_ref}")

                # Remove from global registry (thread-safe)
                with active_actors_lock:
                    active_actors.discard(actor_ref)

                # Remove from websocket mapping (thread-safe)
                with websocket_to_actor_lock:
                    websocket_to_actor.pop(websocket, None)

                print(f"Active actors count after cleanup: {len(active_actors)}")

            except Exception as e:
                print(f"Error during actor cleanup: {e}")

# Optional: Utility functions for managing actors
def get_active_actors_count() -> int:
    """Get the current count of active actors."""
    with active_actors_lock:
        return len(active_actors)

def broadcast_to_all_actors(message: str):
    """Send a message to all active actors."""
    with active_actors_lock:
        for actor_ref in active_actors.copy():  # Copy to avoid modification during iteration
            try:
                actor_ref.tell(message)
            except Exception:
                print(f"The actor is no longer active, removing from registry: {actor_ref}")
                # Optionally remove dead actors
                active_actors.discard(actor_ref)

def stop_all_actors():
    """Stop all active actors (useful for graceful shutdown)."""
    with active_actors_lock:
        for actor_ref in active_actors.copy():
            try:
                actor_ref.stop()
            except Exception as e:
                print(f"Error stopping actor {actor_ref}: {e}")
        active_actors.clear()

    with websocket_to_actor_lock:
        websocket_to_actor.clear()
        
@app.get("/broadcast")
async def broadcast(message: str):
    broadcast_to_all_actors(message)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Optional: Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "active_websockets": len(websocket_to_actor),
        "active_actors": get_active_actors_count()
    }

