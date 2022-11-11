####### PONG #######

# Author: adarax (Discord: adam(cs guy))

# RIP predict(). You will be missed. 2022-2022

import math
import pygame as pg
import random as r

pg.init()
pg.display.set_caption("Pong")

size_x = 9000
size_y = 700
screen = pg.display.set_mode((size_x, size_y), pg.RESIZABLE)

# Ball setup
ball_radius = 20
ball_x = size_x / 2
ball_y = size_y / 2
ball_x_offset = 3 if r.randint(0, 1) == 1 else -3 # randomize starting direction
ball_y_offset = 4

ball_motion_vector = [ball_x_offset, ball_y_offset]

# Size of paddles
paddle_height = 120
paddle_width = 25

# Left paddle coords
l_x = 10
l_y = size_y / 2 - paddle_height / 2

# right paddle coords
r_x = size_x - paddle_width - 10
r_y = size_y / 2 - paddle_height / 2

# Score -> player 1 is right paddle and player 2 is left paddle
player1_score = 0
player2_score = 0

# Score goes up to score_to_win
score_to_win = 10

# font of scoreboard
font = pg.font.SysFont(None, 50)

def draw():
    # Drawing right paddle
    pg.draw.rect(screen, (255, 0, 0), pg.Rect(r_x, r_y, paddle_width, paddle_height))

    # Drawing left paddle
    pg.draw.rect(screen, (255, 0, 0), pg.Rect(l_x, l_y, paddle_width, paddle_height))

    # Drawing ball
    pg.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), ball_radius)

    # Drawing scoreboard
    p1 = font.render(str(player1_score), True, (255, 255, 255))
    p2 = font.render(str(player2_score), True, (255, 255, 255))
    screen.blit(p1, (size_x / 2 + 13, 15))
    screen.blit(p2, (size_x / 2 - 32, 15))

    # Middle line
    pg.draw.line(screen, (255, 255, 255), (size_x / 2, 0), (size_x / 2, size_y))

    pg.display.flip()

draw()

# Generates return angle of ball
def randomAngle():
    temp = ball_motion_vector.copy()
    
    max_range = abs(int(temp[1]))
    min_range = abs(int(temp[1])) * -1
    len_of_temp = math.sqrt(temp[0] ** 2 + temp[1] ** 2)
    
    temp[1] = r.randint(1, max_range) if temp[1] > 0 else r.randint(min_range, -1)
    temp[0] = math.sqrt(len_of_temp ** 2 - temp[1] ** 2) if temp[0] < 0 else math.sqrt(len_of_temp ** 2 - temp[1] ** 2) * -1

    ball_motion_vector[0] = temp[0]
    ball_motion_vector[1] = temp[1]

# Loop setup
run = True
is_paused = False

# Refresh rate: (1000 / speed) = FPS
speed = 10

# Increases ball speed over time by this amount
offset_increase_constant = 0.001

while run:
    pg.time.delay(speed)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()

    # Escape full screen mode
    if keys[pg.K_ESCAPE]:
        if screen == pg.display.set_mode((size_x, size_y), pg.FULLSCREEN):
            screen = pg.display.set_mode((size_x, size_y), pg.RESIZABLE)

    # Enter full screen mode
    if keys[pg.K_f]:
        if screen == pg.display.set_mode((size_x, size_y), pg.RESIZABLE):
            screen = pg.display.set_mode((size_x, size_y), pg.FULLSCREEN)

    if player1_score == score_to_win or player2_score == score_to_win:
        winner = "Player 1 wins!" if player1_score == score_to_win else "Player 2 wins!"
        game_over_message = font.render("Game Over! " + winner, True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(game_over_message, (size_x / 2 - 240, size_y / 2 - 50))
        pg.display.flip()
        pg.time.delay(2000)
        run = False

    # P to pause
    if keys[pg.K_p]:
        is_paused = True
        paused_message = font.render("Paused", True, (255, 255, 255))
        to_resume = font.render("Press R to resume", True, (255, 255, 255))
        screen.blit(paused_message, (size_x / 2 - 63, size_y / 2 - 50))
        screen.blit(to_resume, (size_x / 2 - 130, size_y / 2))
        pg.display.flip()

    # R to unpause
    if is_paused and keys[pg.K_r]:
         is_paused = False

    if not is_paused and run:
        # Increase speed of ball only when game is not paused
        if ball_x_offset < 0:
            ball_x_offset -= offset_increase_constant
        else:
            ball_x_offset += offset_increase_constant

        if ball_y_offset < 0:
            ball_y_offset -= offset_increase_constant
        else:
            ball_y_offset += offset_increase_constant

        ball_x += ball_motion_vector[0]
        ball_y += ball_motion_vector[1]


        # Controls (human controlled right side)
        if keys[pg.K_UP] and not r_y <= 0:
            r_y -= 5
        if keys[pg.K_DOWN] and not r_y + paddle_height >= size_y - 0:
            r_y += 5

        # Controls (human controlled left side)
        if keys[pg.K_w] and not l_y <= 0:
            l_y -= 5
        if keys[pg.K_s] and not l_y + paddle_height >= size_y - 0:
            l_y += 5

        # Normal difficulty: tracks ball
        if ball_motion_vector[1] > 0:
            if l_y + paddle_height / 2 < ball_y:
                if not l_y + paddle_height >= size_y:
                    l_y += 5
        else:
            if l_y + paddle_height / 2 > ball_y:
                if not l_y / 2 <= 0:
                    l_y -= 5

        # Bounce off floor
        if ball_y + ball_radius >= size_y - 3:
            ball_motion_vector[1] = -ball_y_offset

        # Bounce off ceiling
        if ball_y - ball_radius <= 3:
            ball_motion_vector[1] = ball_y_offset

        # Bounce off left paddle
        if ball_x - ball_radius <= 30:
            if ball_y >= l_y and ball_y <= l_y + paddle_height:
                randomAngle()

        # Bounce off right paddle
        if ball_x + ball_radius >= size_x - 30:
            if ball_y >= r_y and ball_y <= r_y + paddle_height:
                randomAngle()

        # If hits either right or left wall
        if ball_x + ball_radius >= size_x or ball_x - ball_radius <= 0:
            # If hits right wall (player 2 scores)
            if ball_x + ball_radius >= size_x - 10:
                player2_score += 1
            else:
                player1_score += 1

            # Reset position (starting left or right depends on who got the point, starts towards scorer's side)
            ball_x = size_x / 2
            ball_y = size_y / 2

            # Reset speed
            ball_x_offset = 3 if r.randint(0, 1) == 1 else -3
            ball_y_offset = 4
            ball_motion_vector = [ball_x_offset, ball_y_offset]

            # Reset animation
            screen.fill((0, 0, 0))
            pg.draw.rect(screen, (255, 0, 0), pg.Rect(r_x, r_y, paddle_width, paddle_height))
            pg.draw.rect(screen, (255, 0, 0), pg.Rect(l_x, l_y, paddle_width, paddle_height))
            p1 = font.render(str(player1_score), True, (255, 255, 255))
            p2 = font.render(str(player2_score), True, (255, 255, 255))
            screen.blit(p1, (size_x / 2 + 13, 15))
            screen.blit(p2, (size_x / 2 - 32, 15))
            pg.draw.line(screen, (255, 255, 255), (size_x / 2, 0), (size_x / 2, size_y))
            pg.display.flip()
            pg.time.delay(400)
            first_predict = True
            continue

        # TODO
        # Instructions before game starts, graphical selection of difficulty and multiplayer mode
        # Retry button after game over
        # Baymax themed ball and paddles

        screen.fill((0, 0, 0))
        draw()

pg.quit()
