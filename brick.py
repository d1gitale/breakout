import pyxel

BrickType = {
    1: {
        "img_bank": 0,
        "u": 16,
        "v": 0,
        "width": 32,
        "height": 8,
        "score": 1
    },
    2: {
        "img_bank": 0,
        "u": 16,
        "v": 8,
        "width": 32,
        "height": 8,
        "score": 2
    },
    3: {
        "img_bank": 0,
        "u": 16,
        "v": 16,
        "width": 32,
        "height": 8,
        "score": 3
    },
    4: {
        "img_bank": 0,
        "u": 16,
        "v": 24,
        "width": 32,
        "height": 8,
        "score": 4
    }
}


class Brick:
    def __init__(self, x, y, brick_type):
        self.x = x
        self.y = y
        self.brick_type = brick_type
        self.width = BrickType[brick_type]["width"]
        self.height = BrickType[brick_type]["height"]
        self.score = BrickType[brick_type]["score"]

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            BrickType[self.brick_type]["img_bank"],
            BrickType[self.brick_type]["u"],
            BrickType[self.brick_type]["v"],
            BrickType[self.brick_type]["width"],
            BrickType[self.brick_type]["height"],
        )


def check_levels():
    with open("assets/levels.txt", "r") as f:
        found_levels = [line.strip() for line in f.readlines()]

    return found_levels


def load_level(level):
    level_data = []
    possible_bricks = ['1', '2', '3', '4']

    with open(f"assets/levels/{level}", "r") as f:
        y = 0
        for line in f:
            x = 0
            for char in line:
                if char in possible_bricks:
                    level_data.append(Brick(x, y, int(char)))

                x += 32
            y += 8
    return level_data