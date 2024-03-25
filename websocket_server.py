import asyncio
import websockets
from typing import Set

class WebSocketServer:
    """
    WebSocketServer class manages WebSocket connections.

    Attributes:
        clients (set): A set to store active WebSocket connections.
    """

    def __init__(self):
        """Initialize WebSocketServer with an empty set of clients."""
        self.clients: Set = set()

    async def echo(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        """
        Asynchronous method to handle incoming WebSocket connections.

        Args:
            websocket (WebSocketServerProtocol): WebSocket connection object.
            path (str): The requested path.

        Notes:
            This method adds the WebSocket connection to the clients set
            and ensures it's removed when the connection is closed.
        """
        self.clients.add(websocket)
        try:
            while True:
                await asyncio.sleep(3600)  
        finally:
            self.clients.remove(websocket)

    async def dispatch(self, message: str) -> None:
        """
        Dispatches a message to all connected clients.

        Args:
            message (str): The message to be dispatched.

        Note:
            This method sends the message to all clients asynchronously.
        """
        for client in self.clients:
            await client.send(message)

