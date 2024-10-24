class Food:
    def __init__(self, id, pos: tuple[int, int, int] = (0, 0, 0)):
        self.id = id
        self.pos = pos
    
    def set_pos(self, pos: tuple[int, int, int]):
        self.pos = pos

    def get_pos(self) -> tuple[int, int, int]:
        return self.pos
    
    def __str__(self):
        return f"Food at {self.pos}"
    
    async def info_to_send(self):
        return {
            "id": self.id,
            "pos": self.pos
        }