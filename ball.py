import pyxel
from math import copysign
from time import sleep


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speedX = -1.0
        self.speedY = -1.5
        self.radius = 2
        self.out_of_bounds = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, 7)

    def update(self):
        self.x += self.speedX
        self.y += self.speedY

        if self.x + self.radius >= pyxel.width:
            self.speedX = -self.speedX
        elif self.x - self.radius <= 0:
            self.speedX = -self.speedX
        if self.y - self.radius <= 0:
            self.speedY = -self.speedY
        elif self.y + self.radius >= pyxel.height:
            self.out_of_bounds = True


    def speedup(self, amount):
        self.speedX += copysign(amount, self.speedX)
        self.speedY += copysign(amount, self.speedY)


    def detect_collision(self, entity, paddle=False):
        score = 0

        num_steps = pyxel.ceil(max(abs(self.speedX), abs(self.speedY)))
        
        if num_steps == 0:
            return False, score

        step_size = 1.0 / num_steps

        for step in range(1, num_steps + 1):
            time = step * step_size
            sub_ball_x = self.x + time * self.speedX
            sub_ball_y = self.y + time * self.speedY

            if (
                sub_ball_x + self.radius >= entity.x
                and sub_ball_x - self.radius <= entity.x + entity.width
                and sub_ball_y + self.radius >= entity.y
                and sub_ball_y - self.radius <= entity.y + entity.height
            ):
                if paddle:
                    self.speedX = entity.deflect_force(self.x)
                    self.speedY = -self.speedY
                else:
                    if sub_ball_x + self.radius >= entity.x > sub_ball_x - self.radius:
                        self.x = entity.x - self.radius
                        self.speedX = -self.speedX
                    elif sub_ball_x - self.radius <= entity.x + entity.width < sub_ball_x + self.radius:
                        self.x = entity.x + entity.width + self.radius
                        self.speedX = -self.speedX
                    elif sub_ball_y + self.radius >= entity.y > sub_ball_y - self.radius:
                        self.y = entity.y - self.radius
                        self.speedY = -self.speedY
                    elif sub_ball_y - self.radius <= entity.y + entity.height < sub_ball_y + self.radius:
                        self.y = entity.y + entity.height + self.radius
                        self.speedY = -self.speedY
                    score += entity.score
                return True, score
                
        return False, score