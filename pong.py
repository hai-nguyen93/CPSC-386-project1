import pygame
import sys
from pygame.locals import *
import random
import objects
import time

SCR_WIDTH = 800
SCR_HEIGHT = 600
SCORES_HEIGHT = SCR_HEIGHT / 6

MOVESPEED = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_text(surface, text, x, y, size=30):
    font = pygame.font.Font(None, size)
    text_render = font.render(text, True, WHITE, BLACK)
    text_rect = text_render.get_rect()
    text_rect.left = x + 20
    text_rect.top = y + 20
    surface.blit(text_render, text_rect)


def reset_ball(ball):
    ball.rect.x = 400
    ball.rect.y = 250
    old_x_velocity = ball.velocity.x
    while True:
        ball.velocity.x = random.randint(-7, 7)
        ball.velocity.y = random.randint(-7, 7)
        # redo if the new velocity is slow, only x-direction, only y-direction
        # or in the same x-direction with the velocity when the ball goes out of the playing area
        if ball.velocity.magnitude() > 5 and abs(ball.velocity.x) > 2 \
                and ball.velocity.y != 0 and old_x_velocity*ball.velocity.x <= 0:
            break
    time.sleep(0.5)  # delay 0.5 second before resuming the game


def play_game(surface):
    main_clock = pygame.time.Clock()
    move_up, move_down, move_left, move_right = False, False, False, False

    # Set up images and ball
    ball_image = pygame.image.load('images/ball.png')
    vertical_paddle_image = pygame.image.load('images/vertical_paddle.png')
    horizontal_paddle_image = pygame.image.load('images/horizontal_paddle.png')
    cpu_vertical_paddle_image = pygame.image.load('images/cpu_vertical_paddle.png')
    cpu_horizontal_paddle_image = pygame.image.load('images/cpu_horizontal_paddle.png')
    ball = objects.Ball(image=ball_image)
    reset_ball(ball)

    # Set up paddles
    player = objects.Score()
    computer = objects.Score()
    player_paddles = [objects.Paddle(SCR_WIDTH - vertical_paddle_image.get_rect().right, 250, vertical_paddle_image),
                      objects.Paddle(round(SCR_WIDTH * 0.75), 0, horizontal_paddle_image, vertical=False),
                      objects.Paddle(round(SCR_WIDTH * 0.75),
                                     SCR_HEIGHT - SCORES_HEIGHT - horizontal_paddle_image.get_rect().bottom,
                                     horizontal_paddle_image, vertical=False)]
    computer_paddles = [objects.Paddle(0, 250, cpu_vertical_paddle_image),
                        objects.Paddle(round(SCR_WIDTH * 0.25), 0, cpu_horizontal_paddle_image, vertical=False),
                        objects.Paddle(round(SCR_WIDTH * 0.25),
                                       SCR_HEIGHT - SCORES_HEIGHT - cpu_horizontal_paddle_image.get_rect().bottom,
                                       cpu_horizontal_paddle_image, vertical=False)]

    # Set up sounds
    ball_sound = pygame.mixer.Sound('audio/pickup.wav')
    game_over = pygame.mixer.Sound('audio/gameover.wav')
    game_win = pygame.mixer.Sound('audio/game_win.wav')
    game_lose = pygame.mixer.Sound('audio/game_lose.wav')

    no_winner = True
    while no_winner:
        pygame.mixer.music.stop()
        # Check for winner
        if player.game_point == 3 or computer.game_point == 3:
            no_winner = False

            # Display winner
            if player.game_point == 3:
                draw_text(surface, 'YOU WON!!!', SCR_WIDTH / 2 - 120, SCORES_HEIGHT, size=50)
                pygame.mixer.music.load('audio/victory.mid')
                pygame.mixer.music.play()
            elif computer.game_point == 3:
                draw_text(surface, 'YOU LOST!!!', SCR_WIDTH / 2 - 130, SCORES_HEIGHT, size=50)
                game_over.play()

            # Play again
            draw_text(surface, 'Play again? (Press Y or N)', SCR_WIDTH / 2 - 136, SCR_HEIGHT / 2 - 40)
            pygame.display.update()
            play_again = False
            while not play_again:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYUP:
                        if event.key == K_y:
                            player.reset()
                            computer.reset()
                            no_winner = True
                            play_again = True
                            reset_ball(ball)
                            break
                        elif event.key == K_n:
                            pygame.quit()
                            sys.exit()

        # Check game score
        if player.point >= 11 and player.point - computer.point >= 2:
            player.game_point += 1
            if player.game_point < 3:
                game_win.play()
                time.sleep(0.7)
            player.point, computer.point = 0, 0
        if computer.point >= 11 and computer.point - player.point >= 2:
            computer.game_point += 1
            if computer.game_point < 3:
                game_lose.play()
                time.sleep(0.7)
            player.point, computer.point = 0, 0

        # Update ball
        ball.move()
        if ball.rect.y + ball.image_rect.centery < 0 \
                or ball.rect.y + ball.image_rect.centery >= SCR_HEIGHT-SCORES_HEIGHT:
            if ball.rect.x + ball.image_rect.centerx <= SCR_WIDTH/2:
                player.point += 1
            else:
                computer.point += 1
            reset_ball(ball)
        if ball.rect.x + ball.image_rect.centerx < 0:
            player.point += 1
            reset_ball(ball)
        if ball.rect.x + ball.image_rect.centerx > SCR_WIDTH:
            computer.point += 1
            reset_ball(ball)

        # Get input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    move_up = True
                if event.key == K_DOWN:
                    move_down = True
                if event.key == K_RIGHT:
                    move_right = True
                if event.key == K_LEFT:
                    move_left = True

            if event.type == KEYUP:
                if event.key == K_UP:
                    move_up = False
                    # player.point += 1
                if event.key == K_DOWN:
                    # computer.point += 1
                    move_down = False
                if event.key == K_RIGHT:
                    move_right = False
                if event.key == K_LEFT:
                    move_left = False

        # Move player's paddles
        if move_up:
            for paddle in player_paddles:
                if paddle.vertical:
                    if paddle.rect.y > 0:
                        paddle.rect.y -= MOVESPEED
                    else:
                        paddle.rect.y = 0
        if move_down:
            for paddle in player_paddles:
                if paddle.vertical:
                    if paddle.rect.y + paddle.image_rect.bottom < SCR_HEIGHT-SCORES_HEIGHT:
                        paddle.rect.y += MOVESPEED
                    else:
                        paddle.rect.y = SCR_HEIGHT - SCORES_HEIGHT - paddle.image_rect.bottom
        if move_left:
            for paddle in player_paddles:
                if not paddle.vertical:
                    if paddle.rect.x > SCR_WIDTH/2:
                        paddle.rect.x -= MOVESPEED
                    else:
                        paddle.rect.x = SCR_WIDTH/2
        if move_right:
            for paddle in player_paddles:
                if not paddle.vertical:
                    if paddle.rect.x + paddle.image_rect.right < SCR_WIDTH:
                        paddle.rect.x += MOVESPEED
                    else:
                        paddle.rect.x = SCR_WIDTH - paddle.image_rect.right

        # Move computer's paddles
        for paddle in computer_paddles:
            if paddle.vertical:
                if ball.rect.y + ball.image_rect.centery < paddle.rect.y + paddle.image_rect.centery - 12:
                    if paddle.rect.y > 0:
                        paddle.rect.y -= (MOVESPEED - 1.5)
                    else:
                        paddle.rect.y = 0
                elif ball.rect.y + ball.image_rect.centery > paddle.rect.y + paddle.image_rect.centery + 12:
                    if paddle.rect.y + paddle.image_rect.bottom < SCR_HEIGHT-SCORES_HEIGHT:
                        paddle.rect.y += (MOVESPEED - 1.5)
                    else:
                        paddle.rect.y = SCR_HEIGHT - SCORES_HEIGHT - paddle.image_rect.bottom
            else:
                if ball.rect.x + ball.image_rect.centerx < paddle.rect.x + paddle.image_rect.centerx - 12:
                    if paddle.rect.x > 0:
                        paddle.rect.x -= (MOVESPEED - 1.5)
                    else:
                        paddle.rect.x = 0
                elif ball.rect.x + ball.image_rect.centerx > paddle.rect.x + paddle.image_rect.centerx + 12:
                    if paddle.rect.x + paddle.image_rect.right < SCR_WIDTH/2:
                        paddle.rect.x += (MOVESPEED - 1.5)
                    else:
                        paddle.rect.x = SCR_WIDTH/2 - paddle.image_rect.right

        # Check for collision
        for paddle in player_paddles:  # player's paddles
            if ball.rect.colliderect(paddle.rect):
                if paddle.vertical:
                    # Adjust the ball before bouncing back
                    ball.rect.x = paddle.rect.x - ball.image_rect.right
                    ball.velocity.x *= -1
                else:
                    # Adjust the ball before bouncing back
                    if paddle.rect.y < 1:  # upper horizontal paddle
                        ball.rect.y = paddle.rect.y + paddle.image_rect.bottom
                    else:  # lower horizontal paddle
                        ball.rect.y = paddle.rect.y - ball.image_rect.bottom
                    ball.velocity.y *= -1
                ball_sound.play()

        for paddle in computer_paddles:  # computer's paddles
            if ball.rect.colliderect(paddle.rect):
                if paddle.vertical:
                    # Adjust the ball before bouncing back
                    ball.rect.x = paddle.rect.x + paddle.image_rect.right
                    ball.velocity.x *= -1
                else:
                    # Adjust the ball before bouncing back
                    if paddle.rect.y < 1:  # upper horizontal paddle
                        ball.rect.y = paddle.rect.y + paddle.image_rect.bottom
                    else:  # lower horizontal paddle
                        ball.rect.y = paddle.rect.y - ball.image_rect.bottom
                    ball.velocity.y *= -1
                ball_sound.play()

        # Draw the screen
        surface.fill(BLACK)
        pygame.draw.line(surface, WHITE, (0, SCR_HEIGHT - SCORES_HEIGHT), (SCR_WIDTH, SCR_HEIGHT - SCORES_HEIGHT))
        pygame.draw.line(surface, WHITE, (SCR_WIDTH / 2, 0), (SCR_WIDTH / 2, SCR_HEIGHT - SCORES_HEIGHT))

        # Draw the scores
        # Calculate points to win current game
        point_to_win_game = [11, 11]   # 1st element is player's point to win game, 2nd element is computer's
        point_to_win_game[0] = 2 + computer.point if (computer.point >= 10) else 11
        point_to_win_game[1] = 2 + player.point if (player.point >= 10) else 11
        # Player's scores
        draw_text(surface, 'Player: {} ({} to win game)'.format(player.point, point_to_win_game[0]),
                  x=SCR_WIDTH/2, y=SCR_HEIGHT-SCORES_HEIGHT)
        draw_text(surface, 'Game point: {} (3 to win match)'.format(player.game_point),
                  x=SCR_WIDTH/2, y=SCR_HEIGHT-SCORES_HEIGHT+40)

        # Computer's score
        draw_text(surface, 'Computer: {} ({} to win game)'.format(computer.point, point_to_win_game[1]),
                  x=0, y=SCR_HEIGHT-SCORES_HEIGHT)
        draw_text(surface, 'Game point: {} (3 to win match)'.format(computer.game_point),
                  x=0, y=SCR_HEIGHT-SCORES_HEIGHT+40)

        # Draw the ball and paddles
        surface.blit(ball_image, (ball.rect.x, ball.rect.y))
        for paddle in computer_paddles:
            surface.blit(paddle.image, (paddle.rect.x, paddle.rect.y))
        for paddle in player_paddles:
            surface.blit(paddle.image, (paddle.rect.x, paddle.rect.y))

        pygame.display.update()
        main_clock.tick(60)


def play():
    pygame.init()
    surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), 0, 32)
    pygame.display.set_caption('Pong')

    surface.fill(BLACK)
    pygame.draw.line(surface, WHITE, (0, SCR_HEIGHT - SCORES_HEIGHT), (SCR_WIDTH, SCR_HEIGHT - SCORES_HEIGHT))
    pygame.draw.line(surface, WHITE, (SCR_WIDTH / 2, 0), (SCR_WIDTH / 2, SCR_HEIGHT - SCORES_HEIGHT))
    pygame.display.update()

    play_game(surface)


play()
