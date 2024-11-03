from fastapi import WebSocket
import json
import time
import asyncio

from model.player import Player
from model.food import Food
from model.trap import Trap

class Game:
    def __init__(self):
        self.players: list[Player] = []
        self.game_state = "waiting_for_players"
        self.foods: dict[int, Food] = {}
        self.traps: list[Trap] = []

    async def add_player(self, websocket: WebSocket):
        player = Player(websocket)
        data = await websocket.receive_text()
        print(data)
        name = json.loads(data)["name"]
        await player.login(str(len(self.players)), name)
        self.players.append(player)
        player.id = str(len(self.players))
        await player.send_json({"code" : 200, "msg": f"login success, now {len(self.players)} players is in the game" })

    async def info_to_send(self):
        players_info = []
        for player in self.players:
            players_info.append(await player.info_to_send())
        
        foods_info = []
        for food_idx, food in self.foods.items():
            foods_info.append(await food.info_to_send())
        return {"players": players_info, "foods": foods_info}
    

    async def process_frame(self, frame_idx):
        # 处理当前帧逻辑
        for player in self.players:
            await player.process_frame(frame_idx)
            for food_idx in player.eaten_food_ids:
                self.foods.pop(food_idx)

        for i in range(len(self.players)):
            for j in range(i+1, len(self.players)):
                if not await self.players[i].check_collision(self.players[j]):
                    continue
                if self.players[i].weight > self.players[j].weight:
                    self.players[i].weight += self.players[j].weight
                    self.players[j].alive = False
                else:
                    self.players[j].weight += self.players[i].weight
                    self.players[i].alive = False


        # 发送当前帧状态
        for player in self.players:
            res = player.send_json({
                "data": await self.info_to_send()})

    async def start_game(self):
        self.game_state = "running"
        for player in self.players:
            res = player.send_json({
                "code" : 200, 
                "msg": "game start", 
                "players": [await p.info_to_send() for p in self.players]})
        frame_idx = 0
        while True:
            start_time = time.time()  # 获取当前时间
            await self.process_frame(frame_idx)  # 执行函数
            elapsed_time = time.time() - start_time  # 计算函数执行所花费的时间
            
            # 计算剩余的时间并等待
            await asyncio.sleep(max(0, 0.1 - elapsed_time))
