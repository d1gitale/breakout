import pyxel
import enum
from ball import Ball
from paddle import Paddle
from brick import Brick
from brick import check_levels, load_level
from hud import *


class GameState(enum.Enum):
    READY = 0
    RUNNING = 1
    DROPPED = 2
    GAME_OVER = 3
    WIN = 4


BRICK_SOUND = 0
PADDLE_SOUND = 1
DROP_SOUND = 2
LOSE_SOUND = 3
WIN_SOUND = 4


class App:
    def __init__(self):
        pyxel.init(width=384, height=300, display_scale=3, title="Breakout", fps=60)
        pyxel.load("assets/resources.pyxres")
        self.levels = check_levels()
        self.ball = Ball()
        self.paddle = Paddle()
        self.reset_ball()
        self.bounces = 0
        self.bricks = None
        self.current_level = None
        self.current_state = None
        self.score = None
        self.lives = None
        self.win_flag = None
        self.start_game()
        pyxel.run(self.update, self.draw)


    def start_game(self):
        self.current_level = 1
        self.score = 0
        self.lives = 3
        self.bricks = load_level(self.levels[self.current_level - 1])
        self.reset_ball()
        self.current_state = GameState.READY


    def reset_ball(self):
        self.ball.x = self.paddle.x + self.paddle.width / 2 + 10
        self.ball.y = self.paddle.y - self.ball.radius
        self.ball.speedX = self.paddle.deflect_force(self.ball.x)
        self.ball.speedY = -2.5
        self.ball.out_of_bounds = False
        self.bounces = 0


    def next_level(self):
        self.current_level += 1
        if self.current_level > len(self.levels):
            self.current_state = GameState.WIN
            pyxel.play(0, WIN_SOUND)
            return
        self.bricks = load_level(self.levels[self.current_level - 1])
        self.current_state = GameState.READY
        self.reset_ball()

    
    def update(self):
        self.check_input()
        self.paddle.update()
        if self.current_state == GameState.READY:
            self.ball.x = self.paddle.x + self.paddle.width / 2
        if self.current_state == GameState.RUNNING:
            self.ball.update()
            self.check_collision()
            if self.ball.out_of_bounds:
                pyxel.play(0, DROP_SOUND)
                self.lives -= 1
                if self.lives > 0:
                    self.current_state = GameState.DROPPED
                else:
                    self.current_state = GameState.GAME_OVER
                    pyxel.play(0, LOSE_SOUND)


    def check_collision(self):
        collision, _ = self.ball.detect_collision(self.paddle, paddle=True)
        
        if collision:
            pyxel.play(0, PADDLE_SOUND)
            self.bounces += 1
            self.check_speedup()

        for i in reversed(range(len(self.bricks))):
            brick = self.bricks[i]
            collision, score = self.ball.detect_collision(brick)
            if collision:
                self.bounces += 1
                self.check_speedup()
                pyxel.play(0, BRICK_SOUND)
                self.score += score
                del self.bricks[i]
                self.check_completion()
                break


    def check_speedup(self):
        if self.bounces == 4:
            self.ball.speedup(1.0)
        if self.bounces == 12:
            self.ball.speedup(2.0)


    def check_completion(self):
        if len(self.bricks) == 0:
            self.next_level()


    def check_input(self):
        if self.current_state == GameState.READY:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.current_state = GameState.RUNNING

        if self.current_state == GameState.DROPPED:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.reset_ball()
                self.current_state = GameState.READY

        if self.current_state == GameState.GAME_OVER or self.current_state == GameState.WIN:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.start_game()

        if pyxel.btnp(pyxel.KEY_TAB):
            self.next_level()

        if pyxel.btnp(pyxel.KEY_H):
            self.lives += 1


    def draw(self):
        pyxel.cls(0)

        self.paddle.draw()

        for brick in self.bricks:
            brick.draw()

        self.ball.draw()

        draw_hud(score=self.score, lives=self.lives)
        
        if self.current_state == GameState.DROPPED:
            draw_dropped()
        elif self.current_state == GameState.GAME_OVER:
            draw_game_over(self.score)
        elif self.current_state == GameState.WIN:
            draw_win()


if __name__ == "__main__":
    App()