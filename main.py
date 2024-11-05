from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
import asyncio
import json

import uvicorn
from game import Game
import threading

app = FastAPI()
game = Game()

async def start_game_in_task():
    print("start game")
    await game.start_game()

def run_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

new_loop = asyncio.new_event_loop()

thread = threading.Thread(target=run_event_loop, args=(new_loop,))

new_loop.create_task(start_game_in_task())

# 存储活动的 WebSocket 连接
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("websocket connected")
    await websocket.accept()
    player_id = await game.add_player()
    player_id -= 1
    print("player added")
    while True:
        await websocket.send_text(game.players[player_id].message_to_send)
        print(game.players[player_id].message_to_send)
        data = await websocket.receive_text()
        print("data:",data)
        data = json.loads(data)
        game.players[player_id].frame_to_process = data
        await asyncio.sleep(0.1)
    

@app.get("/")
async def get():
    # 一个简单的 HTML 页面，显示游戏中所有player的name,pos, weight
    return HTMLResponse(content=f"""
    <html>
        <head>
            <title>Game</title>
        </head>
        <body>
            <h1>Game</h1>
            <div id="game">
                <ul id="players">
                    {"".join(f"<li>{player.name}: {player.pos}, {player.weight}</li>" for player in game.players)}
                </ul>
            </div>
        </body>
    </html>
    """)

@app.post("/start")
async def start():
    await game.start_game()
    return {"message": "Game started"}

@app.get("/players")
async def get_players():
    return {"code":200, "data":[{"name":player.name, "id":player.id }for player in game.players]}

if __name__ == "__main__":
    thread.start()
    uvicorn.run(app, host="0.0.0.0", port=25555)