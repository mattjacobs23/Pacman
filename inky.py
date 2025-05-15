import pygame
import math
from settings import *
from enemy_class import Enemy

vec = pygame.math.Vector2


class Inky(Enemy):
    def __init__(self, app, pos, player, img, blinky):
        super().__init__(app, pos)
        self.color = (163,226,222)
        self.direction = vec(1, 0)
        self.player = player
        self.blinky = blinky
        self.in_ghost_house = True
        self.img = pygame.transform.scale(img, (CELL_WIDTH, CELL_HEIGHT))


    def update(self):
        if len(self.app.coins) < 235:
            if self.in_ghost_house: # manually move left 2 and up 2
                if self.grid_pos.x == 13:
                    self.direction = vec(0, -1)
                if self.grid_pos.y == 11:
                    self.in_ghost_house = False
            else:
                # Find the next direction to move
                next_dir = self.find_next_direction(self.player.grid_pos, self.player.direction, self.blinky.grid_pos)
                if self.time_to_move():
                    if next_dir is not None:
                        self.direction = vec(next_dir[0], next_dir[1])

            # Move
            self.pix_pos += self.direction * self.speed

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + CELL_WIDTH // 2) // CELL_WIDTH + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + CELL_HEIGHT // 2) // CELL_HEIGHT + 1

    def find_next_direction(self, player_pos, player_dir, blinky_pos):
        # Get minimum linear distance from Pinky to 4 steps ahead of Pacman for all possible tiles
        direction_to_move = 0
        min_distance = float("inf")

        # Inky's target tile is based on a line from Blinky to 2 tiles in front of pacman, then extend that line
        # to be double the size.
        x_dist = (player_pos.x + player_dir.x * 2 - blinky_pos.x) * 2

        if x_dist != 0:
            target_slope = (blinky_pos.y - (player_pos.y + player_dir.y * 2)) / (blinky_pos.x - (player_pos.x + player_dir.x * 2))
            x_coord = blinky_pos.x + x_dist
            y_coord = x_dist * target_slope
            target_tile = vec(x_coord, y_coord)

            # Loop through possible directions, check if there is a wall, or ghost house gate
            # Also, ghosts cannot turn around
            for i, dir in enumerate(self.possible_directions):
                next_x, next_y = int(self.grid_pos.x + dir[0]), int(self.grid_pos.y + dir[1])
                # add boundary check here
                map_height = len(self.app.map)
                map_width = len(self.app.map[0])
                if not (0 <= next_x < map_width and 0 <= next_y < map_height):
                    continue

                next_tile = self.app.map[next_y][next_x]
                if dir != self.direction * -1 and next_tile != '1' and next_tile != 'B':
                    distance = math.sqrt((next_x - target_tile.x)**2 + (next_y - target_tile.y)**2)
                    if distance < min_distance:
                        min_distance = distance
                        direction_to_move = i


            return self.possible_directions[direction_to_move]

