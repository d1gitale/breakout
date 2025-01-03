import pyxel


def draw_hud(score=0, lives=0):
    pyxel.text(10, 5, "Score: " + str(score), 7)
    lives_text = "Lives: " + str(lives)
    pyxel.text(right_text(lives_text), 5, lives_text, 7)


def draw_dropped():
    title = "DROPPED THE BALL"
    subtitle = "Click to continue"
    pyxel.text(center_text(title), pyxel.height / 3, title, 7)
    pyxel.text(center_text(subtitle), pyxel.height / 2, subtitle, 7)


def draw_win(score=0):
    title = "YOU WIN!"
    subtitle = "Click to restart"
    pyxel.text(center_text(title), pyxel.height / 3, title, 7)
    pyxel.text(center_text(subtitle), pyxel.height / 2, subtitle, 7)


def draw_game_over(score=0):
    title = "GAME OVER"
    subtitle = f"You scored: {score} points"
    continue_text = "Click to restart"
    pyxel.text(center_text(title), pyxel.height / 3, title, 7)
    pyxel.text(center_text(subtitle), pyxel.height / 12 * 5, subtitle, 7)
    pyxel.text(center_text(continue_text), pyxel.height / 2, continue_text, 7)


def center_text(text, char_width=pyxel.FONT_WIDTH):
    text_width = len(text) * char_width
    return (pyxel.width - text_width) / 2


def right_text(text, char_width=pyxel.FONT_WIDTH):
    text_width = len(text) * char_width
    return pyxel.width - (text_width + char_width)

