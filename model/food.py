import random
N = 50000
class Food:
    def __init__(self, id):
        self.id = id
        random.seed(id)
        self.pos = (random.randint(-N, N), 0, random.randint(-N, N))
        self.exist = True
    
    def set_pos(self, pos: tuple[int, int, int]):
        self.pos = pos

    def get_pos(self) -> tuple[int, int, int]:
        return self.pos
    
    def __str__(self):
        return f"Food at {self.pos}"
    
    async def info_to_send(self):
        return {
            "id": self.id,
            "pos": self.pos,
            "exist": self.exist
        }