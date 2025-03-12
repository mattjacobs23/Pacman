import pygame
from settings import *

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2

    def move(self, direction):
        self.stored_direction = direction

    def update(self):
        # If direction is not leading us to hit a wall, then update position on the screen
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed

        # If we are in the middle of the cell, update our direction with stored_direction
        if self.time_to_move():
            if self.stored_direction is not None and self.can_move(self.stored_direction):
                self.direction = self.stored_direction
            self.able_to_move = self.can_move(self.direction)

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + CELL_WIDTH//2) // CELL_WIDTH + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + CELL_HEIGHT//2) // CELL_HEIGHT + 1

        if self.on_coin():
            self.eat_coin()

    def get_pix_pos(self):
        return vec((self.grid_pos.x * CELL_WIDTH) + TOP_BOTTOM_BUFFER // 2 + CELL_WIDTH // 2,
                   (self.grid_pos.y * CELL_HEIGHT) + TOP_BOTTOM_BUFFER // 2 + CELL_HEIGHT // 2)

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOR, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           CELL_WIDTH // 2 - 2)

        # Drawing the grid position rect
        #pygame.draw.rect(self.app.screen, RED, (
        #self.grid_pos[0] * CELL_WIDTH + TOP_BOTTOM_BUFFER // 2, self.grid_pos[1] * CELL_HEIGHT + TOP_BOTTOM_BUFFER // 2,
        #CELL_WIDTH, CELL_HEIGHT), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if self.time_to_move():
                return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1


    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER//2) % CELL_WIDTH == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True

        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % CELL_HEIGHT == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True

        return False

    def can_move(self, dir):
        next_x, next_y = int(self.grid_pos.x + dir[0]), int(self.grid_pos.y + dir[1])
        next_tile = self.app.map[next_y][next_x]
        return next_tile not in ('1', 'B')