import pyxel


class Paddle:
    def __init__(self):
        self.width = 48
        self.height = 8
        self.x = pyxel.width / 2 - self.width / 2
        self.y = pyxel.height - 50
        self.mid_sections = 4
        self.sprite_img_bank = 0
        self.sprite_width = 8
        self.sprite_height = 8
        self.sprite_edge_u = 8
        self.sprite_edge_v = 0
        self.sprite_mid_u = 0
        self.sprite_mid_v = 8

    def draw(self):
        pyxel.blt(
            self.x,
            self.y,
            self.sprite_img_bank,
            self.sprite_edge_u,
            self.sprite_edge_v,
            self.sprite_width,
            self.sprite_height
        )

        for i in range(1, self.mid_sections + 1):
            pyxel.blt(
                self.x + (self.sprite_width * i),
                self.y,
                self.sprite_img_bank,
                self.sprite_mid_u,
                self.sprite_mid_v,
                self.sprite_width,
                self.sprite_height
            )

        pyxel.blt(
            self.x + self.sprite_width * (self.mid_sections + 1),
            self.y,
            self.sprite_img_bank,
            self.sprite_edge_u,
            self.sprite_edge_v,
            self.sprite_width,
            self.sprite_height,
            rotate=180
        )

    def update(self):
        self.x = min(pyxel.width - self.width, max(0, pyxel.mouse_x))

    def deflect_force(self, u):
        force = (u - (self.x + self.width / 2)) / 10
        return force
