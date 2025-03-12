import pygame
import math
from settings import *
from enemy_class import Enemy

vec = pygame.math.Vector2


class Clyde(Enemy):
    def __init__(self, app, pos, player, img):
        super().__init__(app, pos)
        self.color = (255, 213, 128)
        self.direction = vec(-1, 0)
        self.player = player
        self.in_ghost_house = True
        self.img = pygame.transform.scale(img, (CELL_WIDTH, CELL_HEIGHT))


    def update(self):
        if len(self.app.coins) < 190:
            if self.in_ghost_house: # manually move left 2 and up 2
                if self.grid_pos.x == 13:
                    self.direction = vec(0, -1)
                if self.grid_pos.y == 11:
                    self.in_ghost_house = False
            else:
                # Find the next direction to move
                if self.time_to_move():
                    # If we are far from pacman, chase pacman
                    if abs(self.grid_pos.x - self.player.grid_pos.x) > 8 or abs(self.grid_pos.y - self.player.grid_pos.y) > 8:
                        next_dir = self.chase_find_next_direction(self.player.grid_pos)
                    else:
                        next_dir = self.scatter_find_next_direction()
                    self.direction = vec(next_dir[0], next_dir[1])

            # Move
            self.pix_pos += self.direction * self.speed

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + CELL_WIDTH // 2) // CELL_WIDTH + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + CELL_HEIGHT // 2) // CELL_HEIGHT + 1


    def chase_find_next_direction(self, player_pos):
        # Get minimum linear distance from Clyde to Pacman for all possible tiles
        direction_to_move = 0
        min_distance = float("inf")

        # Loop through possible directions, check if there is a wall, or ghost house gate
        # Also, ghosts cannot turn around
        # If that is all ok, find linear path to pacman, return minimum from all these possible tiles
        for i, dir in enumerate(self.possible_directions):
            next_x, next_y = int(self.grid_pos.x + dir[0]), int(self.grid_pos.y + dir[1])
            next_tile = self.app.map[next_y][next_x]
            if dir != self.direction * -1 and next_tile != '1' and next_tile != 'B':
                distance = math.sqrt((next_x - player_pos.x) ** 2 + (next_y - player_pos.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    direction_to_move = i

        return self.possible_directions[direction_to_move]


    def scatter_find_next_direction(self):
        # Get minimum linear distance from Clyde to Pacman for all possible tiles
        direction_to_move = 0
        min_distance = float("inf")

        # bottom left corner is the target tile
        target_tile = vec(1, 30)

        # Loop through possible directions, check if there is a wall, or ghost house gate
        # Also, ghosts cannot turn around
        # If that is all ok, find linear path to pacman, return minimum from all these possible tiles
        for i, dir in enumerate(self.possible_directions):
            next_x, next_y = int(self.grid_pos.x + dir[0]), int(self.grid_pos.y + dir[1])
            next_tile = self.app.map[next_y][next_x]
            if dir != self.direction * -1 and next_tile != '1' and next_tile != 'B':
                distance = math.sqrt((next_x - target_tile.x) ** 2 + (next_y - target_tile.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    direction_to_move = i

        return self.possible_directions[direction_to_move]

