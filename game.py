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
        self.foods: list[Food] = []
        self.traps: list[Trap] = []

    async def add_player(self):
        player = Player()
        await player.login(str(len(self.players)+1))
        self.players.append(player)
        return len(self.players)

    async def info_to_send(self):
        players_info = []
        for player in self.players:
            players_info.append(await player.info_to_send())
        
        foods_info = []
        for food in self.foods:
            if food.exist:
                foods_info.append(await food.info_to_send())
        return {"players": players_info, "foods": foods_info}
    
    def is_eaten(self, food, player):
        return (player.pos[0]-food.pos[0])**2 + (player.pos[1]-food.pos[1])**2 + (player.pos[2]-food.pos[2])**2 < player.weight**2

    async def process_frame(self, frame_idx):
        # 处理当前帧逻辑
        for player in self.players:
            await player.process_frame(frame_idx)
            for food in self.foods:
                if self.is_eaten(food,player):
                    food.exist = False
                    player.weight += 1000

        for i in range(len(self.players)):
            for j in range(i+1, len(self.players)):
                if not await self.players[i].check_collision(self.players[j]):
                    continue
                if self.players[i].weight > self.players[j].weight:
                    self.players[i].weight += self.players[j].weight
                    self.players[j].weight = 0
                    self.players[j].alive = False
                else:
                    self.players[j].weight += self.players[i].weight
                    self.players[j].weight = 0
                    self.players[i].alive = False

        # 生成新的食物
        if frame_idx % 10 == 0 and len(self.foods) < 10 and len(self.players) > 0:
            self.foods.append(Food(str(len(self.foods))))

        # 发送当前帧状态
        for player in self.players:
            await player.send_json({
                "data": await self.info_to_send()})

    async def start_game(self):
        self.game_state = "running"
        frame_idx = 0
        while True:
            # print("frame", frame_idx)
            start_time = time.time()  # 获取当前时间
            await self.process_frame(frame_idx)  # 执行函数
            elapsed_time = time.time() - start_time  # 计算函数执行所花费的时间
            
            # 计算剩余的时间并等待
            time.sleep(max(0, 0.1 - elapsed_time))
            frame_idx += 1
