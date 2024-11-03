from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
import asyncio
from game import Game

app = FastAPI()
game = Game()

# 存储活动的 WebSocket 连接
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("websocket connected")
    await websocket.accept()
    # await game.add_player(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # 接收消息
            await websocket.send_text(f"Message received: {data}")  # 发送消息
    except WebSocketDisconnect:
        print("Client disconnected")  # 客户端断开连接
    

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