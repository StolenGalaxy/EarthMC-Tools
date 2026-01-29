class Player:
    def __init__(self):
        self.name = ""
        self.coords = ""

        self.is_visible = True
        self.time_since_visible = 0


class Coordinates:
    def __init__(self, X: int, Y: int, Z: int):
        self.X = X
        self.Y = Y
        self.Z = Z
