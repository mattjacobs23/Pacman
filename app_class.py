import pygame, sys
from settings import *
from player_class import *
from enemy_class import *
from blinky import *
from pinky import *
from inky import *
from clyde import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.map = []  # 2d array for ghosts to use to find path to pacman
        self.p_pos = None
        self.load()
        self.player = Player(self, self.p_pos)
        self.make_enemies()
        self.game_start_time = 0  # keep track of when player starts the game
        self.hit_by_ghost = False

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                if self.hit_by_ghost:
                    self.end_screen(player_won=False)
                else:
                    self.playing_events()
                    self.playing_update()
                    self.playing_draw()
            elif self.state == 'player_won':
                self.end_screen(player_won=True)
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


    ############################# HELPER FUNCTIONS ###################################
    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        with open("walls.txt", 'r') as file:
            for y_idx, line in enumerate(file):
                new_list = []
                for x_idx, char in enumerate(line):
                    new_list.append(char)

                    if char == 'C':
                        self.coins.append(vec(x_idx, y_idx))
                    if char == 'P':
                        self.p_pos = vec(x_idx, y_idx)
                    if char in ["2", "3", "4", "5"]:
                        self.e_pos.append(vec(x_idx, y_idx))
                    if char == 'B':
                        pygame.draw.rect(self.background, BLACK, (x_idx*CELL_WIDTH, y_idx*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

                self.map.append(new_list)



    def make_enemies(self):
        for i, pos in enumerate(self.e_pos):
            if i == 0:
                img = pygame.image.load('imgs/blinky.png').convert_alpha()
                blinky = Blinky(self, pos, self.player, img)
                self.enemies.append(blinky)
            elif i == 1:
                img = pygame.image.load('imgs/pinky.png').convert_alpha()
                self.enemies.append(Pinky(self, pos, self.player, img))
            elif i == 2:
                img = pygame.image.load('imgs/inky.png').convert_alpha()
                self.enemies.append(Inky(self, pos, self.player, img, blinky))
            else:
                img = pygame.image.load('imgs/clyde.png').convert_alpha()
                self.enemies.append(Clyde(self, pos, self.player, img))


    def draw_grid(self):
        for x in range(WIDTH // CELL_WIDTH):
            pygame.draw.line(self.background, GREY, (x * CELL_WIDTH, 0), (x * CELL_WIDTH, HEIGHT))
        for y in range(HEIGHT // CELL_HEIGHT):
            pygame.draw.line(self.background, GREY, (0, y * CELL_HEIGHT), (WIDTH, y * CELL_HEIGHT))
        for coin in self.coins:
            pygame.draw.rect(self.background, (167, 179, 34),
                             (coin.x * CELL_WIDTH, coin.y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    ############################# START FUNCTIONS ###################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'
                self.hit_by_ghost = False
                self.game_start_time = pygame.time.get_ticks()

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH // 2, HEIGHT // 2], START_TEXT_SIZE, (170, 132, 58),
                       START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH // 2, HEIGHT // 2 + 50], START_TEXT_SIZE, (44, 167, 198),
                       START_FONT, centered=True)
        self.draw_text('HIGH SCORE: 0', self.screen, [4, 0], START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()

    ############################# PLAYING FUNCTIONS ###################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            if self.player.grid_pos == enemy.grid_pos:
                self.hit_by_ghost = True

        if len(self.coins) == 0:
            self.state = 'player_won'


    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        # self.draw_grid()
        self.draw_text(f'CURRENT SCORE: {self.player.current_score}', self.screen, [60, 0], 18, WHITE, START_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH // 2 + 60, 0], 18, WHITE, START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw(enemy.color)
        pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7), (
                int(coin.x * CELL_WIDTH) + CELL_WIDTH // 2 + TOP_BOTTOM_BUFFER//2, int(coin.y * CELL_HEIGHT) + CELL_HEIGHT // 2 + TOP_BOTTOM_BUFFER//2), 5)



    ############################# GAME OVER ###################################

    def end_screen(self, player_won: bool = False) -> None:
        if player_won:
            text = 'YOU WON!'
        else:
            text = 'YOU LOST :('

        self.screen.fill(BLACK)
        self.draw_text(text, self.screen, [WIDTH//2, HEIGHT//2 - 100], 36, WHITE, START_FONT, centered=True)
        self.draw_text('PUSH SPACE BAR TO PLAY AGAIN', self.screen, [WIDTH//2, HEIGHT//2 + 100], 28, WHITE, START_FONT, centered=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__init__()



