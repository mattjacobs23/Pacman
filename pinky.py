import pygame
import math
from settings import *
from enemy_class import Enemy

vec = pygame.math.Vector2


class Pinky(Enemy):
    def __init__(self, app, pos, player, img):
        super().__init__(app, pos)
        self.color = (255, 105, 180)
        self.direction = vec(-1, 0)
        self.player = player
        self.in_ghost_house = True
        self.img = pygame.transform.scale(img, (CELL_WIDTH, CELL_HEIGHT))


    def update(self):
        if pygame.time.get_ticks() > self.app.game_start_time + 3000:
            if self.in_ghost_house: # manually move left 2 and up 2
                if self.grid_pos.x == 14:
                    self.direction = vec(0, -1)
                if self.grid_pos.y == 11:
                    self.in_ghost_house = False
            else:
                # Find the next direction to move
                next_dir = self.find_next_direction(self.player.grid_pos, self.player.direction)
                if self.time_to_move():
                    self.direction = vec(next_dir[0], next_dir[1])

            # Move
            self.pix_pos += self.direction * self.speed

        # Setting grid position in reference to pix position
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + CELL_WIDTH // 2) // CELL_WIDTH + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + CELL_HEIGHT // 2) // CELL_HEIGHT + 1

    def find_next_direction(self, player_pos, player_dir):
        # Get minimum linear distance from Pinky to 4 steps ahead of Pacman for all possible tiles
        direction_to_move = 0
        min_distance = float("inf")
        num_tiles_ahead = 7

        target_tile = player_pos + (player_dir * num_tiles_ahead)

        # Loop through possible directions, check if there is a wall, or ghost house gate
        # Also, ghosts cannot turn around
        # If that is all ok, find linear path to pacman, return minimum from all these possible tiles
        for i, dir in enumerate(self.possible_directions):
            next_x, next_y = int(self.grid_pos.x + dir[0]), int(self.grid_pos.y + dir[1])
            next_tile = self.app.map[next_y][next_x]
            if dir != self.direction * -1 and next_tile != '1' and next_tile != 'B':
                distance = math.sqrt((next_x - target_tile.x)**2 + (next_y - target_tile.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    direction_to_move = i
                # If Pinky is within 8 tiles of pacman, make target tile pacman instead of 7 tiles ahead of him
                if distance < 6:
                    target_tile = player_pos
                else:
                    target_tile = player_pos + (player_dir * num_tiles_ahead)


        return self.possible_directions[direction_to_move]


