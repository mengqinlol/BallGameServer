from fastapi import WebSocket
import json
import asyncio

class Player:
    def __init__(self, websocket: WebSocket):
        self.id = ''
        self.name = ''
        self.pos = (0, 0, 0)
        self.websocket = websocket
        self.connected = True
        self.alive = True
        self.weight = 5
        self.frame_to_process = None
        self.eaten_food_ids = []
        
    async def listen(self):
        while self.connected:
            data = await self.websocket.receive_text()
            data = json.loads(data)
            '''
            data:
            {
                'frame_idx': xxx,
                'id': xxx,
                'pos': (x, y, z)
            }
            '''
            self.frame_to_process = data

    async def login(self, id: str):
        self.id = id
        asyncio.create_task(self.listen())

    async def disconnect(self):
        self.connected = False
        await self.websocket.close()

    async def send_message(self, message: str):
        if self.connected: 
            res = self.websocket.send_text(message)

    def set_position(self, pos: tuple[int, int, int]):
        self.pos = pos
    
    def get_position(self):
        return self.pos
    
    async def send_json(self, data: dict):
        res = self.send_message(json.dumps(data))

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

    def distance_between(self, pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5

    async def check_collision(self, other_player):
        return self.distance_between(self.pos, other_player.pos) <= self.weight / 2 + other_player.weight / 2
    
