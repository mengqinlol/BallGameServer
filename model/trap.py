class Trap:
    def __init__(self, pos: tuple[int, int, int] = (0, 0, 0)):
        self.pos = pos
        
    def get_pos(self):
        return self.pos

    def set_pos(self, pos: tuple[int, int, int]):
        self.pos = pos

    def __str__(self):
        return f"Trap at {self.pos}"
