from maze import Maze
from Caracter import Player, Ghost
import time 


CELL = 80


class Game:

    def __init__(self, width=15, height=15, perfect=False, seed=42):

        self.width = width
        self.height = height
        self.seed = seed
        self.start = (width // 2, height // 2)

        
        self.start_pix = (((width// 2) * CELL) + CELL // 2, (height // 2) * CELL + CELL // 2 )
        # self.player_position = self.start
        self.corners = [(0, 0), (width - 1, height - 1), (width - 1, 0), (0, height - 1)]
        # self.maze = Maze(width, height, perfect,seed)
        # self.grid = self.maze.grid
        # self.player = Player((width // 2, height // 2), None)
        # self.ghosts = [Ghost((0, 0), None), Ghost((width - 1, height - 1), None),
        #     Ghost((width - 1, 0), None), Ghost((0, height - 1), None)]

        # for ghost in self.ghosts:
        #     ghost.start_pos =  ghost.pos

        # self.gums = self.gums_placement()
        # self.super_gums = self.super_gums()
        # self.edible_active_unitl = 0.0

        # self.visited = set()
        self.lives = 3
        self.score = 0
        self.stop = False
        
        self.level = 1
        self.levels_frames = [24, 24, 22, 22, 20, 20, 18, 18, 16, 16]
        
        self.speed_boost_active = False
        self.random_per = [3, 4, 5, 6, 7, 8, 9, 10, 20, 100]
        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen_active = False

        self.levels_seeds = [42, 14, 26, 39, 52, 78, 71, 84, 93, 11]
        self.initialize_level()

        # self.frames_per_cell = 24

        # self.coeficient = 4

        self.game_over = False
        # self.level_completed = False
        
        # level_expires_at = time.monotonic() + 180
        self.game_won = False



    def initialize_level(self):
        self.player_position = self.start

        self.maze = Maze(self.width, self.height, False, self.levels_seeds[self.level - 1])
        self.grid = self.maze.grid
        self.player = Player((self.width // 2, self.height // 2), None)
        self.ghosts = [Ghost((0, 0), None), Ghost((self.width - 1, self.height - 1), None),
            Ghost((self.width - 1, 0), None), Ghost((0, self.height - 1), None)]


        self.coeficient = 4
        for ghost in self.ghosts:
            ghost.start_pos =  ghost.pos
            ghost.frames_per_cell = self.levels_frames[self.level - 1]
            ghost.coefecient = self.random_per[self.level - 1]
        self.gums = self.gums_placement()
        self.super_gums = self.super_gum()
        self.edible_active_unitl = 0.0
        self.visited = set()
        self.level_completed = False
        self.level_expires_at = time.monotonic() + 1000
        self.game_paused = False
        self.pause_started_at = None

    def Next_level(self):
        self.level += 1

        if self.level > 2:
            self.game_won = True
            self.game_over = True
            return


        self.initialize_level()

        
    def does_level_completed(self):
        if not self.gums and not self.super_gums:
            self.level_completed = True
            # self.level += 1
            return True
        elif time.monotonic() >= self.level_expires_at:
            self.level_completed = True
            # self.level += 1
            return True
        return False
    
    def succesfully_complete_level(self):
        if not self.gums and not self.super_gums:
            return True
        return False
    
        



    def gums_placement(self):
        gums = set()

        reachable = self.maze.get_reachable_cells(self.start)


        for i in range(self.width):
            for item in range(self.height):
                cell = (i, item)

                if cell in reachable and cell not in self.corners and cell != self.start:
                    gums.add(cell)

        
        return gums


    def super_gum(self):
        return set(self.corners)

    def collect_gums(self):
        if self.player.target_pos is not None:
            return
        if self.player.pos not in self.visited:

            if self.player.pos in self.gums:
                self.score += 10
                self.visited.add(self.player.pos)
                self.gums.remove(self.player.pos)
            elif self.player.pos in self.super_gums:
                self.score += 50
                self.visited.add(self.player.pos)
                self.super_gums.remove(self.player.pos)
                for g in self.ghosts:
                    g.state = "EDIBLE"
                self.edible_active_unitl = time.monotonic() + 100
    

    def detect_collision(self):
        for g in self.ghosts:
            dx = self.player.x_pix - g.x_pix
            dy = self.player.y_pix - g.y_pix
            collision =  dx * dx + dy * dy <= (20 + 20) ** 2
            if collision:
                return g
        return None

    def handle_collisions(self):
        g = self.detect_collision()
        if  g is not None:
            if g.state == "DANGEROUS":
                if not self.invincible:
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over = True
                        return
                    self.player.pos = self.start
                    self.player.target_pos = None
                    self.player.direction = None
                    self.player.requested_direction = None
                    self.player.previous_pos = None
                    

                    self.player.x_pix = self.player.pos[0] * CELL + CELL / 2
                    self.player.y_pix = self.player.pos[1] * CELL + CELL / 2

                    for i, gos in enumerate(self.ghosts):
                        gos.pos = self.corners[i]
                        gos.x_pix = gos.pos[0] * CELL + CELL / 2
                        gos.y_pix = gos.pos[1] * CELL + CELL / 2
                        gos.target_pos = None
                        gos.direction = None
                        gos.previous_pos = None
                        gos.state = "DANGEROUS"
                        gos.respawn_time_at = 0.0
                    self.edible_active_unitl = 0.0

            elif g.state == "EDIBLE":
                g.pos = g.start_pos
                g.x_pix = g.pos[0] * CELL + CELL / 2
                g.y_pix = g.pos[1] * CELL + CELL / 2
                g.target_pos = None
                g.direction = None
                g.previous_pos = None
                g.state = "RESPAWNING"
                g.respawn_time_at = time.monotonic() + 10
                self.score += 200
            elif g.state == "RESPAWNING":
                pass

                

    
    def ghost_update(self):
        now = time.monotonic()
        if self.edible_active_unitl and now >= self.edible_active_unitl:
            for gost in self.ghosts:
                if gost.state == "EDIBLE":
                    gost.state = "DANGEROUS"
            self.edible_active_unitl = 0.0

        for g in self.ghosts:
            if g.state == "RESPAWNING" and g.respawn_time_at and now >= g.respawn_time_at:
                g.respawn_time_at = 0.0
                g.state = "DANGEROUS"
    
    def pause_option(self):
        self.game_paused = True
        self.pause_started_at = time.monotonic()
    
    def resume_game(self):
        paused_time = time.monotonic() - self.pause_started_at
        self.level_expires_at += paused_time

        if self.edible_active_unitl:
            self.edible_active_unitl += paused_time
        
        for g in self.ghosts:
            if g.state == "Respawn":
                g.respawn_time_at += paused_time


        self.game_paused =False
        self.pause_started_at = None



    def switch_to_cheat_mode(self):
        self.cheat_mode = True
    
    def switch_to_normal_mode(self):
        self.cheat_mode = False
        self.invincible = False
        self.speed_boost_active = False
        self.speed_boost()
        self.ghosts_frozen_active =False
        

    def iron_man(self):
        if self.cheat_mode:
            self.invincible = not self.invincible

    def add_life(self):
        if self.cheat_mode:
            self.lives += 1


    def speed_boost(self):
        if self.cheat_mode:
            self.speed_boost_active = not self.speed_boost_active
        
        if self.speed_boost_active:
            self.player.frames_per_cell = max(
                1,
                self.player.normal_frames_per_cell // 2
            )
        else:
            self.player.frames_per_cell = self.player.normal_frames_per_cell


    def ghost_freeze(self):
        if self.cheat_mode:
            self.ghosts_frozen_active = not self.ghosts_frozen_active
        
        

    