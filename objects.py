import pygame


class Ball:
    def __init__(self, image):
        self.velocity = pygame.math.Vector2()
        self.velocity.x = 0
        self.velocity.y = 0
        self.image = image
        self.image_rect = image.get_rect()
        self.rect = pygame.Rect(0, 0, self.image_rect.right, self.image_rect.bottom)

    def move(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y


class Paddle:
    def __init__(self, x, y, image, vertical=True):
        self.image = image
        self.vertical = vertical
        self.image_rect = image.get_rect()
        self.rect = pygame.Rect(x, y, self.image_rect.right, self.image_rect.bottom)


class Score:
    def __init__(self):
        self.point = 0
        self.game_point = 0

    def reset(self):
        self.point, self.game_point = 0, 0
