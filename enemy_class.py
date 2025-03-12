import pygame
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.color = (255, 0, 0)
        self.pix_pos = self.get_pix_pos()
        self.radius = int(CELL_WIDTH // 2.3)
        self.speed = 1.25
        self.possible_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]


    def get_pix_pos(self):
        return vec((self.grid_pos.x * CELL_WIDTH) + TOP_BOTTOM_BUFFER // 2 + CELL_WIDTH // 2,
                   (self.grid_pos.y * CELL_HEIGHT) + TOP_BOTTOM_BUFFER // 2 + CELL_HEIGHT // 2)

    def update(self):
        pass

    def draw(self, color):
        # pygame.draw.circle(self.app.screen, color, (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)
        self.app.screen.blit(self.img, (int(self.pix_pos.x - CELL_WIDTH // 2), int(self.pix_pos.y - CELL_WIDTH // 2)))



    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER//2) % CELL_WIDTH == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % CELL_HEIGHT == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True
        return False


    def can_move(self):
        next_x, next_y = int(self.grid_pos.x + self.direction[0]), int(self.grid_pos.y + self.direction[1])
        next_tile = self.app.map[next_y][next_x]
        return next_tile not in ('1', 'B')


