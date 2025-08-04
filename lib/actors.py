import asyncio
import threading
from pykka import ThreadingActor
from fastapi import WebSocket

class ActorWsMessageSender(ThreadingActor):
    def __init__(self, websocket: WebSocket):
        """_summary_
        Note do not instantiate this directly.
        Do WebSocketReceiveActor.start(websocket) instead.

        Args:
            websocket (WebSocket): _description_

        Raises:
            ValueError: _description_
        """
        super().__init__() # be sure to do this.
        if not websocket:
            raise ValueError("WebSocket cannot be None")
        self.websocket = websocket
        self.name = f"WebSocketActor-{id(websocket)}"
        self.loop = None
        self.loop_thread = None

    def on_start(self):
        # We need to start a dedicated event loop to send messages
        # to the WebSocket client.
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self.loop.run_forever, daemon=True)
        self.loop_thread.start()

    def on_stop(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.loop_thread:
            self.loop_thread.join()

    def on_receive(self, message: str):
        if not self.loop or not self.loop.is_running():
            print("Event loop not available in actor")
            return
        try:
            # Send message to the WebSocket client
            asyncio.run_coroutine_threadsafe(self._send_to_websocket(message), self.loop)
        except Exception as e:
            print(f"Error submitting task to event loop: {e}")

    async def _send_to_websocket(self, message: str):
        try:
            await self.websocket.send_text(message)
        except Exception as e:
            print(f"Failed to send to WebSocket or local event loop not running: {e}")
            # WebSocket might be closed, consider stopping this actor
            self.stop()
            
            