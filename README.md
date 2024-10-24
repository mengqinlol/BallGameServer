# BallGameServer
## 客户端对接流程

- 客户端连接服务器
客户端向/ws建立socket连接

- 客户端发送用户信息
客户端建立连接后立刻发送用户注册信息
```json
{
    "name": "wjx",
}
```
服务器返回成功信息
```json
{
    "code" : 200,
    "msg": "login success, now xx players is in the game"
}
```
- 客户端开始游戏
客户端向/start 发送http post请求即开始游戏

- 进行游戏
客户端每tick向服务器发送玩家信息
```json
{
    "frame_idx": 0,
    "id": 0,
    "pos": [1,2,3],
    "eaten_food_ids": [0, 2, 3]
}
```
服务器返回当前帧信息
```json
{
    "frame_idx": 0,
    "data":{
        "players": 
        [
            {
                "id": 0,
                "pos": [1,2,3],
                "weight": 10,
                "alive": true
            },
            {
                "id": 1,
                "pos": [4,5,6],
                "weight": 20,
                "alive": true
            }
        ],
        "foods": [
            {
                "id": 0,
                "pos": [7,8,9]
            },
            {
                "id": 1,
                "pos": [10,11,12]
            }
        ]
        }
    
}
```
其中，吃食物逻辑由客户端判定，服务器负责计算玩家之间的碰撞
所有玩家体重增加由服务器计算
换而言之
客户端需要处理的逻辑如下：
- 玩家移动
- 玩家吃食物

服务端给客户端的信息如下：
- 玩家列表(id,位置,体重,是否存活)
- 食物列表(id,位置)

客户端需要渲染的信息如下：
- 玩家位置
- 玩家体重
- 玩家是否存活
- 食物位置
