from fastapi import WebSocket
from uuid import uuid4

from exceptions import BadContent


class ConnectionManager:
    def __init__(self):
        self.active_connections = dict()
        self.user_states = dict()

    async def connect(self, websocket: WebSocket):
        unique_id = str(uuid4())[:10]
        await websocket.accept()
        self.active_connections[unique_id] = websocket
        self.user_states[unique_id] = dict()
        print(f"User {unique_id} connected.")
        return unique_id

    def disconnect(self, unique_id):
        if unique_id in self.active_connections:
            del self.active_connections[unique_id]
            del self.user_states[unique_id]
            print(f"User {unique_id} disconnected.")

    async def send_message(self, unique_id, message):
        if unique_id in self.active_connections:
            await self.active_connections[unique_id].send_text(message)

    def get_user_state(self, unique_id):
        user = self.user_states.get(unique_id, None)
        if user is None:
            raise BadContent()
        return self.user_states[unique_id].get("user_state", None)

    def modify_user_state(self, unique_id, state):
        if state == "":
            self.user_states[unique_id].pop("user_state", None)
        else:
            self.user_states[unique_id]["user_state"] = state