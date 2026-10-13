import pygame
from mazegenerator import MazeGenerator
from maze import Maze
from Game import Game

CREAM = (245, 230, 205)
LABEL = (190, 170, 160)
GOLD = (255, 200, 80)
CRIMSON = (200, 40, 50)
WOOD = (92, 62, 40)
WOOD_DARK = (60, 40, 28)


BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)     # Pac-Man
ORANGE_42: tuple[int, int, int] = (219, 70, 4)       # walls
RED: tuple[int, int, int] = (255, 0, 0)          # Blinky
PINK: tuple[int, int, int] = (255, 184, 255)     # Pinky
CYAN: tuple[int, int, int] = (0, 255, 255)       # Inky
ORANGE: tuple[int, int, int] = (255, 184, 82)    # Clyde


ROWS = 21
COLS = 21

CELL = 80

SEED = 42

WIDTH = ROWS * CELL
HEIGHT = COLS * CELL

PADDING = 40
GAP = 20
SIDEBAR_WIDTH = 700

WINDOW_WIDTH = PADDING + WIDTH + GAP + SIDEBAR_WIDTH + PADDING
WINDOW_HEIGHT = PADDING + HEIGHT + PADDING

FPS = 60
STEP = 40


class Visual:

    def __init__(self):

        self.cell = 40
        self.game = Game(ROWS, COLS, perfect=False, seed=SEED)
        (self.center_x, self.center_y) = self.game.player_position

        self.player_img = None

        self.player_right = None
        self.player_left = None
        self.facing = "right"

        self.heart_full = None
        self.heart_empty = None

        self.ghost1_img = None
        self.supergum_img = None
        self.gum_img = None
        self.timer_img = None
        self.board_img = None

        self.ghost_imgs = []

    def load_maze(self):
        return self.game.grid

    def has_wall(self, cell, side):
        return (cell & side) != 0

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

    def load_images(self):
        self.player_img = self.load_scaled("assets/player.png", CELL - 4)
        self.supergum_img = self.load_scaled("assets/supergum.png", CELL // 2)
        self.gum_img = self.load_scaled("assets/gum.png", CELL // 3)
        self.timer_img = self.load_scaled("assets/timer_sign.png", 300)
        self.timer_font = pygame.font.SysFont("dejavusansmono", 36, bold=True)
        self.board_img = self.load_scaled("assets/board.png", 600)

        bangers = "assets/fonts/Bangers-Regular.ttf"
        self.timer_font = self.load_font(bangers, 40)
        self.label_font = self.load_font(bangers, 35)
        self.value_font = self.load_font(bangers, 54)

        self.player_right = self.load_scaled("assets/player/player1.png", CELL - 8)
        self.player_left = self.load_scaled("assets/player/player2.png", CELL - 8)

        ghost_files = ["assets/ghosts/ghost1.png", "assets/ghosts/ghost2.png",
                       "assets/ghosts/ghost3.png", "assets/ghosts/ghost4.png"]

        self.ghost_imgs = [self.load_scaled(path, CELL - 8)
                           for path in ghost_files]

        self.heart_full = self.load_scaled("assets/lives/full_heart.png", 90)
        self.heart_empty = self.load_scaled("assets/lives/empty_heart.png", 90)

    def draw_lives(self, sidebar_sur, lives, y, max_lives=3):

        w = sidebar_sur.get_width()
        hearth_w = self.heart_full.get_width() if self.heart_full else 40
        gap = 12
        row_w = max_lives * hearth_w + (max_lives - 1) * gap
        x = (w - row_w) // 2

        for i in range(max_lives):
            img = self.heart_full if i < lives else self.heart_empty
            if img is not None:
                sidebar_sur.blit(img, (x, y))
            else:
                color = (220, 40, 60) if i < lives else (80, 80, 90)
                pygame,draw,circle(sidebar_sur, color, (x + 20, y + 20), 18)
            x += hearth_w + gap

        return y + 100

    
    def draw_player(self, maze_sur):

        player = self.game.player
        center = (round(player.x_pix), round(player.y_pix))

        if player.direction in ("left", "right"):
            self.facing = player.direction

        img = self.player_left if self.facing == "left" else self.player_right

        if img is not None:
             maze_sur.blit(img, img.get_rect(center=center))
        else:
            pygame.draw.circle(maze_sur, ORANGE, center, 20)

        # if self.player_img is not None:
        #     rect = self.player_img.get_rect(center=center)
        #     maze_sur.blit(self.player_img, rect)
        # else:
        #     pygame.draw.circle(maze_sur, ORANGE, center, 20)

    def ghosts(self, maze_sur):

        for (x, y) in self.game.corners:
            x_position = (x * CELL) + (CELL / 2)
            y_position = (y * CELL) + (CELL / 2)
            pygame.draw.circle(maze_sur, RED, (x_position, y_position), 20)

    # def draw_ghosts(self, maze_sur):
    #     colors = (RED, PINK, CYAN, ORANGE)

    #     for i, ghost in enumerate(self.game.ghosts):
    #         pygame.draw.circle(
    #             maze_sur,
    #             colors[i % len(colors)],
    #             (round(ghost.x_pix), round(ghost.y_pix)),
    #             20,
    #         )

    def draw_ghosts(self, maze_sur):
        colors = (RED, PINK, CYAN, ORANGE)

        for i, ghost in enumerate(self.game.ghosts):
            center = (round(ghost.x_pix), round(ghost.y_pix))
            img = self.ghost_imgs[i % len(self.ghost_imgs)]

            if img is not None:
                maze_sur.blit(img, img.get_rect(center=center))
            else:
                pygame.draw.circle(maze_sur, colors[i % len(colors)],
                                   center, 20)

    def draw_supergums(self, maze_sur):

        for (x, y) in self.game.super_gums:
            center = (x * CELL + CELL // 2, y * CELL + CELL // 2)

            if self.supergum_img is not None:
                rect = self.supergum_img.get_rect(center=center)
                maze_sur.blit(self.supergum_img, rect)
            else:
                pygame.draw.circle(maze_sur, YELLOW, center, 10)

    def draw_gums(self, maze_sur):

        for (col, row) in self.game.gums:

            center = (col * CELL + CELL // 2, row * CELL + CELL // 2)

            if self.gum_img is not None:
                rect = self.gum_img.get_rect(center=center)
                maze_sur.blit(self.gum_img, rect)
            else:
                pygame.draw.circle(maze_sur, WHITE, center, 4)

    def draw_42_cells(self, maze_sur):

        cells_42 = self.game.maze.get_42_cells()

        for (col, row) in cells_42:
            pygame.draw.rect(maze_sur, ORANGE_42, (col * CELL, row * CELL, CELL, CELL))

    def draw_maze(self, maze_sur, ROWS, COLS, SEED):

        maze = self.load_maze()

        for row, line in enumerate(maze):
            for col, cell in enumerate(line):

                left = CELL * col
                top = CELL * row
                right = left + CELL
                bottom = top + CELL

                if self.has_wall(cell, 1):
                    pygame.draw.line(maze_sur, WHITE, (left, top), (right, top), 2)
                if self.has_wall(cell, 2):
                    pygame.draw.line(maze_sur, WHITE, (right, top), (right, bottom), 2)
                if self.has_wall(cell, 4):
                    pygame.draw.line(maze_sur, WHITE, (left, bottom), (right, bottom), 2)
                if self.has_wall(cell, 8):
                    pygame.draw.line(maze_sur, WHITE, (left, top), (left, bottom), 2)

    def draw_maze_side_bar(self, sidebar_sur):

        rect = sidebar_sur.get_rect()

        pygame.draw.rect(sidebar_sur, WHITE, rect, 2,
                         border_top_right_radius=20,
                         border_bottom_right_radius=20)
        self.draw_timer(sidebar_sur, 90)
        y = 200

        score = self.game.score

        y = self.draw_board(sidebar_sur, "SCORE", f"{score:01d}", y)
        y = self.draw_board(sidebar_sur, "HIGH SCORE", "0048200", y)
        y = self.draw_board(sidebar_sur, "LEVEL", "03 / 10", y)
        y = self.draw_board(sidebar_sur, "LIVES", "", y, lives=self.game.lives)

        board_h = self.board_img.get_height() if self.board_img else 135
        hearts_y = y - board_h // 2 - 5
        y = self.draw_lives(sidebar_sur, self.game.lives, hearts_y)

    def draw_timer(self, sidebar_sur, time_left):
        w = sidebar_sur.get_width()
        minutes, seconds = divmod(int(time_left), 60)
        text = self.timer_font.render(f"{minutes:02d}:{seconds:02d}",
                                      True, (60, 40, 28))

        if self.timer_img is not None:
            rect = self.timer_img.get_rect(midtop=(w // 2, 4))
            sidebar_sur.blit(self.timer_img, rect)
            offset_x = 40
            sidebar_sur.blit(text, text.get_rect(center=(rect.centerx + offset_x, rect.centery)))
        else:
            sidebar_sur.blit(text, text.get_rect(midtop=(w // 2, 30)))

    def draw_board(self, sidebar_sur, label, value, y, lives=None):
        w = sidebar_sur.get_width()
        brown = (60, 40, 28)

        if self.board_img is not None:
            rect = self.board_img.get_rect(midtop=(w // 2, y))
            sidebar_sur.blit(self.board_img, rect)
        else:
            rect = pygame.Rect(0, 0, 300, 135)
            rect.midtop = (w // 2, y)
            pygame.draw.rect(sidebar_sur, (200, 150, 100), rect, 0, 10)

        label_img = self.label_font.render(label, True, brown)
        value_img = self.value_font.render(value, True, brown)
        sidebar_sur.blit(label_img, label_img.get_rect(
            center=(rect.centerx, rect.centery - 32)))
        sidebar_sur.blit(value_img, value_img.get_rect(
            center=(rect.centerx, rect.centery + 10)))

        return rect.bottom - 15

    def run(self):

        pygame.init()

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.load_images()

        maze_sur = pygame.Surface((WIDTH + 2, HEIGHT + 2), pygame.SRCALPHA)
        sidebar_sur = pygame.Surface((SIDEBAR_WIDTH, HEIGHT), pygame.SRCALPHA)

        background = pygame.image.load("assets/background.jpeg").convert()
        background = pygame.transform.smoothscale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption("PAC-MAN")
        clock = pygame.time.Clock()

        running = True
        while running:
            direction = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        direction = "right"
                    elif event.key == pygame.K_UP:
                        direction = "up"
                    elif event.key == pygame.K_DOWN:
                        direction = "down"

            if direction is not None:
                self.game.player.request_direction(direction)

            self.game.player.choose_direction(self.game.maze)

            player = self.game.player

            moved = player.update(self.game.maze)

            for ghost in self.game.ghosts:
                ghost.choose_direction(self.game.maze, self.game.player.pos)
                ghost.frames_per_cell = 24
                ghost.update(self.game.maze)
            if not self.game.game_over:

                self.game.handle_collisions()
            if self.game.game_over:
                pass
                # print("Game oveeeeeeeeeeeeeeeeeeeer!!!!!")

            self.game.collect_gums()

            # maze_sur.fill(BLACK)
            maze_sur.fill((0, 0, 0, 120))
            sidebar_sur.fill((0, 0, 0, 70))

            # screen.fill(BLACK)
            screen.blit(background, (0, 0))

            self.draw_42_cells(maze_sur)

            self.draw_maze(maze_sur, ROWS, COLS, SEED)

            self.draw_gums(maze_sur)
            self.draw_supergums(maze_sur)

            self.draw_player(maze_sur)
            self.draw_ghosts(maze_sur)

            self.draw_maze_side_bar(sidebar_sur)

            screen.blit(maze_sur, (PADDING, PADDING))
            screen.blit(sidebar_sur, (PADDING + WIDTH + GAP, PADDING))

        
            pygame.display.flip()

            clock.tick(FPS)

        pygame.quit()


def main():
    app = Visual()
    app.run()


main()