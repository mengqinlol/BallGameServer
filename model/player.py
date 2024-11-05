from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio

class Player:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.pos = (0, 0, 0)
        self.connected = True
        self.alive = True
        self.weight = 1000
        self.frame_to_process = None
        self.eaten_food_ids = []
        self.message_to_send = ""

    async def login(self, id: str):
        self.id = id
        await self.send_json({"id": id })

    async def send_message(self, message: str):
        self.message_to_send = message

    def set_position(self, pos: tuple[int, int, int]):
        self.pos = pos
    
    def get_position(self):
        return self.pos
    
    async def send_json(self, data: dict):
        await self.send_message(json.dumps(data))

    async def info_to_send(self):
        return {
            'id': self.id,
            'pos': self.pos,
            'weight': self.weight,
            'alive': self.alive
        }
    
    async def process_frame(self, frame_idx: int):
        if self.frame_to_process is not None:
            self.pos = self.frame_to_process['pos']
            self.frame_to_process = None

    async def process(self, data: dict):
        self.pos = data['pos']

    def distance_between(self, pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5

    async def check_collision(self, other_player):
        return self.distance_between(self.pos, other_player.pos) <= self.weight / 2 + other_player.weight / 2
    
