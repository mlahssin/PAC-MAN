import pygame
from mazegenerator import MazeGenerator
from scenes.base import Scene
from maze import Maze
from Game import Game

ROWS = 11
COLS = 11
CELL = 80
SEED = 42

PADDING = 40
GAP = 20
SIDEBAR_WIDTH = 700

MAZE_WIDTH = ROWS * CELL
MAZE_HEIGHT = COLS * CELL

GAME_WIDTH = PADDING + MAZE_WIDTH + GAP + SIDEBAR_WIDTH + PADDING
GAME_HEIGHT = PADDING + MAZE_HEIGHT + PADDING

WHITE = (255, 255, 255)
BROWN = (60, 40, 28)
ORANGE_42 = (219, 70, 4)


FONT = "assets/fonts/Bangers-Regular.ttf"


class GameScene(Scene):

    size = (GAME_WIDTH, GAME_HEIGHT)

    def __init__(self, app):
        super.__init__(app)

        self.game = None
        self.facing = "right"
        self.direction = None

        self.load_images()

        self.player_right = self.load_image("assets/player/player1.png", CELL - 8)
        self.player_left = self.load_image("assets/player/player2.png", CELL - 8)
        self.ghost_imgs = [self.load_image(f"assets/ghosts/ghost{i}.png", CELL - 8) for i in range(1, 5)]

        self.gum_img = self.load_image("assets/gum.png", CELL // 3)
        self.supergum_img = self.load_image("assets/supergum.png", CELL // 2)
        self.timer_img = self.load_image("assets/timer_sign.png", 300)
        self.board_img = self.load_image("assets/board.png", 600)
        self.heart_full = self.load_image("assets/lives/full_heart.png", 90)
        self.heart_empty = self.load_image("assets/lives/empty_heart.png", 90)

        try:
            self.background = pygame.image.load(
                "assets/background.jpeg").convert()
            self.background = pygame.transform.smoothscale(
                self.background, (GAME_WIDTH, GAME_HEIGHT))
            self.timer_font = pygame.font.Font(FONT, 40)
            self.label_font = pygame.font.Font(FONT, 35)
            self.value_font = pygame.font.Font(FONT, 54)

        except (pygame.error, FileNotFoundError):
            print("Error: could not load game assets")
            self.app.running = False

        self.maze_sur = pygame.Surface((MAZE_WIDTH + 2, MAZE_HEIGHT + 2), pygame.SRCALPHA)
        self.sidebar_sur = pygame.Surface((SIDEBAR_WIDTH, MAZE_HEIGHT), pygame.SRCALPHA)

    def on_enter(self):
        self.game = Game(ROWS, COLS, perfect=False, seed=SEED)
        self.direction = None
        self.facing = "right"

    def load_image(self, path, size):
        """Load an image and scale its biggest side to size. None if missing."""
        try:
            img = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            print(f"Warning: could not load {path}")
            return None
        scale = size / max(img.get_width(), img.get_height())
        new_size = (round(img.get_width() * scale), round(img.get_height() * scale))
        return pygame.transform.smoothscale(img, new_size)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.direction = "left"
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.direction = "right"
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.direction = "up"
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.direction = "down"
        elif event.key == pygame.K_ESCAPE:
            self.app.change_scene("menu")

    def update(self, dt):
        game = self.game

        if self.direction is not None:
            game.player.request_direction(self.direction)
            self.direction = None

        game.player.choose_direction(game.maze)
        game.player.update(game.maze)
        game.collect_gums()
        game.ghost_update()

        for ghost in game.ghosts:
            ghost.choose_direction(game.maze, game.player.pos)
            ghost.frames_per_cell = 24
            ghost.update(game.maze)

        game.handle_collisions()

        if game.does_level_completed():
            if game.succesfully_complete_level():
                game.Next_level()
            else:
                game.initialize_level()

        if game.game_over or game.game_won:
            self.app.change_scene("game_over")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # maze layer
        self.maze_sur.fill((0, 0, 0, 120))
        self.draw_42_cells()
        self.draw_walls()
        self.draw_gums()
        self.draw_supergums()
        self.draw_player()
        self.draw_ghosts()
        screen.blit(self.maze_sur, (PADDING, PADDING))

        # sidebar layer
        self.sidebar_sur.fill((0, 0, 0, 70))
        self.draw_sidebar()
        screen.blit(self.sidebar_sur, (PADDING + MAZE_WIDTH + GAP, PADDING))

    def load_scaled(self, path, size):
        try:
            img = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            return None
        scale = size / max(img.get_width(), img.get_height())
        return pygame.transform.smoothscale(
            img, (round(img.get_width() * scale),
                  round(img.get_height() * scale)))

    def load_font(self, path, size):
        try:
            return pygame.font.Font(path, size)
        except (pygame.error, FileNotFoundError, OSError):
            return pygame.font.SysFont("dejavusans", size, bold=True)

    def cell_center(self, col, row):
        return (col * CELL + CELL // 2, row * CELL + CELL // 2)

    def draw_42_cells(self):
        for (col, row) in self.game.maze.get_42_cells():
            pygame.draw.rect(self.maze_sur, ORANGE_42,
                             (col * CELL, row * CELL, CELL, CELL))

    def draw_walls(self):
        for row, line in enumerate(self.game.grid):
            for col, cell in enumerate(line):
                left = col * CELL
                top = row * CELL
                right = left + CELL
                bottom = top + CELL

                if cell & 1:    # north
                    pygame.draw.line(self.maze_sur, WHITE, (left, top), (right, top), 2)
                if cell & 2:    # east
                    pygame.draw.line(self.maze_sur, WHITE, (right, top), (right, bottom), 2)
                if cell & 4:    # south
                    pygame.draw.line(self.maze_sur, WHITE, (left, bottom), (right, bottom), 2)
                if cell & 8:    # west
                    pygame.draw.line(self.maze_sur, WHITE, (left, top), (left, bottom), 2)

    def draw_gums(self):
        for (col, row) in self.game.gums:
            center = self.cell_center(col, row)
            if self.gum_img:
                self.maze_sur.blit(self.gum_img, self.gum_img.get_rect(center=center))
            else:
                pygame.draw.circle(self.maze_sur, WHITE, center, 4)

    def draw_supergums(self):
        for (col, row) in self.game.super_gums:
            center = self.cell_center(col, row)
            if self.supergum_img:
                self.maze_sur.blit(self.supergum_img,
                                   self.supergum_img.get_rect(center=center))
            else:
                pygame.draw.circle(self.maze_sur, (255, 255, 0), center, 10)

    def draw_player(self):
        player = self.game.player
        center = (round(player.x_pix), round(player.y_pix))

        if player.direction in ("left", "right"):
            self.facing = player.direction

        img = self.player_left if self.facing == "left" else self.player_right
        if img:
            self.maze_sur.blit(img, img.get_rect(center=center))
        else:
            pygame.draw.circle(self.maze_sur, (255, 184, 82), center, 20)

    def draw_ghosts(self):
        colors = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]

        for i, ghost in enumerate(self.game.ghosts):
            center = (round(ghost.x_pix), round(ghost.y_pix))
            img = self.ghost_imgs[i % 4]
            if img:
                self.maze_sur.blit(img, img.get_rect(center=center))
            else:
                pygame.draw.circle(self.maze_sur, colors[i % 4], center, 20)

    def draw_sidebar(self):
        pygame.draw.rect(self.sidebar_sur, WHITE, self.sidebar_sur.get_rect(), 2,
                         border_top_right_radius=20, border_bottom_right_radius=20)

        self.draw_timer(90)

        y = 200
        y = self.draw_board("SCORE", str(self.game.score), y)
        y = self.draw_board("HIGH SCORE", "0048200", y)
        y = self.draw_board("LEVEL", "03 / 10", y)
        y = self.draw_board("LIVES", "", y)

        # hearts go inside the LIVES board
        board_h = self.board_img.get_height() if self.board_img else 135
        self.draw_hearts(y - board_h // 2 - 5)

    def draw_timer(self, time_left):
        center_x = SIDEBAR_WIDTH // 2
        minutes, seconds = divmod(int(time_left), 60)
        text = self.timer_font.render(f"{minutes:02d}:{seconds:02d}", True, BROWN)

        if self.timer_img:
            rect = self.timer_img.get_rect(midtop=(center_x, 4))
            self.sidebar_sur.blit(self.timer_img, rect)
            self.sidebar_sur.blit(text, text.get_rect(
                center=(rect.centerx + 40, rect.centery)))
        else:
            self.sidebar_sur.blit(text, text.get_rect(midtop=(center_x, 30)))

    def draw_board(self, label, value, y):
        """Draw one board (label + value). Returns the y for the next board."""
        center_x = SIDEBAR_WIDTH // 2

        if self.board_img:
            rect = self.board_img.get_rect(midtop=(center_x, y))
            self.sidebar_sur.blit(self.board_img, rect)
        else:
            rect = pygame.Rect(0, 0, 300, 135)
            rect.midtop = (center_x, y)
            pygame.draw.rect(self.sidebar_sur, (200, 150, 100), rect, 0, 10)

        label_img = self.label_font.render(label, True, BROWN)
        value_img = self.value_font.render(value, True, BROWN)
        self.sidebar_sur.blit(label_img, label_img.get_rect(
            center=(rect.centerx, rect.centery - 32)))
        self.sidebar_sur.blit(value_img, value_img.get_rect(
            center=(rect.centerx, rect.centery + 10)))

        return rect.bottom - 15

    def draw_hearts(self, y, max_lives=3):
        heart_w = self.heart_full.get_width() if self.heart_full else 40
        gap = 12
        x = (SIDEBAR_WIDTH - (max_lives * heart_w + (max_lives - 1) * gap)) // 2

        for i in range(max_lives):
            img = self.heart_full if i < self.game.lives else self.heart_empty
            if img:
                self.sidebar_sur.blit(img, (x, y))
            else:
                color = (220, 40, 60) if i < self.game.lives else (80, 80, 90)
                pygame.draw.circle(self.sidebar_sur, color, (x + 20, y + 20), 18)
            x += heart_w + gap