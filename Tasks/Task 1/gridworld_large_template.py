import numpy as np
import pygame as pg

#Constants
WIDTH = 750     # width of the environment (px)
HEIGHT = 750    # height of the environment (px)
CENTER = 6
#START_Y, START_X = 0,0
TS = 10         # delay in msec
NC = 50          # number of cells in the environment
cellSize = WIDTH // NC

# define colors
goal_color = pg.Color(0, 100, 0)
start_color = pg.Color(100, 0, 0)
bg_color = pg.Color(0, 0, 0)
wall_color = pg.Color(225, 217, 209)
lava_color = pg.Color(255, 69, 0)
wind_color = pg.Color(50, 205, 50)
hole_color = pg.Color(105, 105, 105)

line_color = pg.Color(128, 128, 128)
agent_color = pg.Color(120,120,0)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

matrix = np.zeros((50,50), int)

wind = [(16,5), (17,5), (18,5), (19,5), (20,5), (21,5), (16,6), (17,6), (18,6), (19,6), (20,6), (21,6), (16,7), (17,7), (18,7), (19,7), (20,7), (21,7), (28,22), (29,22), (30,22), (31,22), (32,22), (33,22),
        (34,22), (35,22), (36,22), (37,22), (38,22), (39,22), (35,7), (36,7), (37,7), (35,8), (36,8), (37,8), (35,9), (36,9), (37,9), (2,29), (2,30), (2,31), (2,32), (2,33), (2,34), (2,35), (2,36), (2,37),
        (2,38), (2,39), (2,40), (2,41), (2,42), (2,43), (2,44), (2,45), (3,29), (3,30), (3,31), (3,32), (3,33), (3,34), (3,35), (3,36), (3,37), (3,38), (3,39), (3,40), (3,41), (3,42), (3,43), (3,44), (3,45),
        (27,39), (27,40), (27,41), (27,42), (27,43), (27,44), (27,45), (27,46), (28,39), (28,40), (28,41), (28,42), (28,43), (28,44), (28,45), (28,46), (29,39), (29,40), (29,41), (29,42), (29,43), (29,44),
        (29,45), (29,46), (30,39), (30,40), (30,41), (30,42), (30,43), (30,44), (30,45), (30,46), (35,30), (36,30), (37,30), (38,30), (35,31), (36, 31), (37,31), (38,31), (35,32), (36,32), (37,32), (38,32),
        (35,33), (36,33), (37,33), (38,33)]

wall = [(45,22), (46,22), (47,22), (48,22), (49,22), (44,21), (45,21), (46,21), (47,21), (48,21), (49,21), (45,26), (46,26), (47,26), (48,26), (49,26), (44,27), (45,27), (46,27), (47,27), (48,27), (49,27),
        (11,3), (11,4), (11,5), (11,6), (11,7), (11,8), (11,9), (11,10), (11,11), (11,12), (11,13), (11,14), (11,15), (11,16), (11,17), (11,18), (11,19),
        (11,20), (12,3), (12,4), (12,5), (12,6), (12,7), (12,8), (12,9), (12,10), (12,11), (12,12), (12,13), (12,14), (12,15), (12,16), (12,17), (12,18), (12,19), (12,20), (31,3), (31,4), (32,3), (32,4),
        (33,3), (33,4), (34,3), (34,4), (35,3), (35,4), (36,3), (36,4), (37,3), (37,4), (38,3), (38,4), (39,3), (39,4), (40,3), (40,4), (41,3), (41,4),
        (31,13), (32,13), (31,14), (32,14), (31,15), (32,15), (31,16), (32,16), (31,17), (32,17),
        (31,18), (32,18), (31,19), (32,19), (31,20), (32,20), (33,19), (32,19), (33,19), (34,19), (35,19), (36,19), (37,19), (38,19), (39,19), (40,19), (41,19), (42,19), (43,19), (33,20), (34,20), (35,20),
        (36,20), (37,20), (38,20), (39,20), (40,20), (41,20), (42,20), (43,20), (5,28), (6,28), (7,28), (8,28), (9,28), (10,28), (11,28), (12,28), (13,28), (14,28), (15,28), (16,28), (17,28), (18,28), (5,29),
        (6,29), (7,29), (8,29), (9,29), (10,29), (11,29), (12,29), (13,29), (14,29), (15,29), (16,29), (17,29), (18,29), (17,30), (18,30), (17,31), (18,31), (17,32), (18,32), (17,33), (18,33), (17,34), (18,34),
        (17,35), (18,35), (17,36), (18,36), (17,37), (18,37), (17,38), (18,38), (17,39), (18,39), (17,40), (18,40), (17,41), (18,41), (17,42), (18,42), (17,43), (18,43), (17,44), (18,44), (17,45), (18,45),
        (17,46), (18,46), (5,45), (6,45), (7,45), (8,45), (9,45), (10,45), (11,45), (12,45), (13,45),
        (14,45), (15,45), (16,45), (5,46), (6,46), (7,46), (8,46), (9,46), (10,46), (11,46), (12,46), (13,46), (14,46), (15,46), (16,46), (42,28), (43,28), (42,29), (43,29), (42,30), (43,30), (42,31), (43,31),
        (42,32), (43,32), (42,33), (43,33), (42,34), (43,34), (42,35), (43,35), (42,36), (43,36), (42,37), (43,37), (42,38), (43,38), (42,39), (43,39), (42,40), (43,40), (42,41), (43,41), (42,42), (43,42),
        (42,43), (43,43), (42,44), (43,44), (42,45), (43,45), (42,46), (43,46), (31,28), (32,28), (31,29), (32,29), (31,30), (32,30), (31,31), (32,31), (31,32), (32,32), (31,33), (32,33), (31,34), (32,34),
        (31,35), (32,35), (31,36), (32,36), (31,37), (32,37), (33,36), (34,36), (35,36), (36,36), (37,36), (38,36), (39,36), (40,36), (41,36), (33,37), (34,37), (35,37), (36,37), (37,37), (38,37), (39,37), (40,37),
        (41,37),
        (13,19), (14,19), (15,19), (16,19), (17,19), (18,19), (19,19), (20,19), (21,19), (22,19), (23,19), (24,19), (25,19), (26,19), (27,19), (28,19), (29,19), (30,19), (31,19),
        (13,20), (14,20), (15,20), (16,20), (17,20), (18,20), (19,20), (20,20), (21,20), (22,20), (23,20), (24,20), (25,20), (26,20), (27,20), (28,20), (29,20), (30,20), (31,20)
        ]

lava = [(4,8), (4,9), (4,10), (4,11), (4,12), (4,13), (4,14), (4,15), (4,16), (4,17), (5,8), (5,9), (5,10), (5,11), (5,12), (5,13), (5,14), (5,15), (5,16), (5,17), (5,8), (5,9), (5,10), (5,11), (5,12), (5,13),
        (5,14), (5,15), (5,16), (5,17), (27,5), (27,6), (27,7), (27,8), (27,9), (27,10), (27,11), (27,12), (27,13), (28,5), (28,6), (28,7), (28,8), (28,9), (28,10), (28,11), (28,12), (28,13), (29,5), (29,6),
        (29,7), (29,8), (29,9), (29,10), (29,11), (29,12), (29,13), (38,15), (39,15), (40,15), (41,15), (42,15), (43,15), (44,15), (45,15), (46,15), (38,16), (39,16), (40,16), (41,16), (42,16), (43,16), (44,16),
        (45,16), (46,16), (38,17), (39,17), (40,17), (41,17), (42,17), (43,17), (44,17), (45,17), (46,17), (10,32), (11,32), (10,33), (11,33), (10,34), (11,34), (10,35), (11,35), (8,48), (9,48), (10,48), (11,48),
        (12,48), (13,48), (14,48), (15,48), (16,48), (17,48),
        (11,0), (12,0), (11,1), (12,1), (11,2), (12,2)
        ]

hole = [(18,16), (19,16), (18,17), (19,17), (3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5),
        (40,7), (41,7), (42,7), (43,7), (44,7), (45,7), (40,8), (41,8), (42,8), (43,8), (44,8), (45,8), (40,9), (41,9), (42,9), (43,9), (44,9), (45,9),
        (40,10), (41,10), (42,10), (43,10), (44,10), (45,10), (40,11), (41,11), (42,11), (43,11), (44,11), (45,11), (40,12), (41,12), (42,12), (43,12), (44,12), (45,12),
        (21,29), (22,29), (23,29), (24,29), (25,29), (26,29), (27,29), (28,29), (29,29), (21,30), (22,30), (23,30), (24,30), (25,30), (26,30), (27,30), (28,30), (29,30),
        (21,31), (22,31), (23,31), (24,31), (25,31), (26,31), (27,31), (28,31), (29,31), (21,32), (22,32), (23,32), (24,32), (25,32), (26,32), (27,32), (28,32), (29,32),
        (21,33), (22,33), (23,33), (24,33), (25,33), (26,33), (27,33), (28,33), (29,33), (21,34), (22,34), (23,34), (24,34), (25,34), (26,34), (27,34), (28,34), (29,34),
        (21,35), (22,35), (23,35), (24,35), (25,35), (26,35), (27,35), (28,35), (29,35), (21,36), (22,36), (23,36), (24,36), (25,36), (26,36), (27,36), (28,36), (29,36),
        (21,37), (22,37), (23,37), (24,37), (25,37), (26,37), (27,37), (28,37), (29,37),
        (45,35), (46,35), (47,35), (48,35), (49,35), (45,36), (46,36), (47,36), (48,36), (49,36), (45,37), (46,37), (47,37), (48,37), (49,37),
        (45,38), (46,38), (47,38), (48,38), (49,38), (45,39), (46,39), (47,39), (48,39), (49,39)
        ]


for i in range(len(wind)):
    matrix[wind[i][1], wind[i][0]] = 1

for i in range(len(wall)):
    matrix[wall[i][1], wall[i][0]] = 2

for i in range(len(lava)):
    matrix[lava[i][1], lava[i][0]] = 3

for i in range(len(hole)):
    matrix[hole[i][1], hole[i][0]] = 4

#print(matrix)

def draw_grid(screen):
    blockSize = 15
    blockFill = WIDTH // NC
    blockCount = HEIGHT/50
    '''a function to draw gridlines and other objects'''
    # draw goal states
    pg.draw.rect(screen, goal_color, (49 * blockFill, 24 * blockFill, blockFill, blockCount))

    # draw goal walls
    pg.draw.rect(screen, wall_color, (45 * blockFill, 21 * blockFill, 5 * blockFill, 2 * blockCount))
    pg.draw.rect(screen, wall_color, (45 * blockFill, 26 * blockFill, 5 * blockFill, 2 * blockCount))
    pg.draw.rect(screen, wall_color, (44 * blockFill, 21 * blockFill, 1 * blockFill, 1 * blockCount))
    pg.draw.rect(screen, wall_color, (44 * blockFill, 27 * blockFill, 1 * blockFill, 1 * blockCount))

    # draw start state
    pg.draw.rect(screen, start_color, (0, 0, blockFill, blockCount))

    #wall
    pg.draw.rect(screen, wall_color, (13 * blockFill, 19 * blockFill, 18 * blockFill, 2 * blockCount))

    # 1
    pg.draw.rect(screen, wall_color, (11 * blockFill, 3 * blockFill, 2 * blockFill, 18 * blockCount))
    # lava
    pg.draw.rect(screen, lava_color, (4 * blockFill, 8 * blockFill, 2 * blockFill, 10 * blockCount))
    pg.draw.rect(screen, lava_color, (11 * blockFill, 0 * blockFill , 2 * blockFill, 3 * blockCount))
    # wind
    pg.draw.rect(screen, wind_color, (16 * blockFill, 5 * blockFill, 6 * blockFill, 3 * blockCount))
    # hole
    pg.draw.rect(screen, hole_color, (18 * blockFill, 16 * blockFill, 2 * blockFill, 2 * blockCount))
    pg.draw.rect(screen, hole_color, (3 * blockFill, 3 * blockFill, 3 * blockFill, 3 * blockCount))
    pg.draw.rect(screen, hole_color, (40 * blockFill, 7 * blockFill, 6 * blockFill, 6 * blockCount))
    pg.draw.rect(screen, hole_color, (21 * blockFill, 29 * blockFill, 9 * blockFill, 8 * blockCount))
    pg.draw.rect(screen, hole_color, (45 * blockFill, 35 * blockFill, 5 * blockFill, 4 * blockCount))

    # 2
    pg.draw.rect(screen, wall_color, (31 * blockFill, 3 * blockFill, 13 * blockFill, 2 * blockCount))
    #pg.draw.rect(screen, wall_color, (42 * blockFill, 5 * blockFill, 2 * blockFill, 8 * blockCount))
    #pg.draw.rect(screen, wall_color, (31 * blockFill, 11 * blockFill, 13 * blockFill, 2 * blockCount))
    pg.draw.rect(screen, wall_color, (31 * blockFill, 11 * blockFill, 2 * blockFill, 8 * blockCount))
    pg.draw.rect(screen, wall_color, (31 * blockFill, 19 * blockFill, 13 * blockFill, 2 * blockCount))
    # lava
    pg.draw.rect(screen, lava_color, (27 * blockFill, 5 * blockFill, 3 * blockFill, 9 * blockCount))
    pg.draw.rect(screen, lava_color, (38 * blockFill, 15 * blockFill, 9 * blockFill, 3 * blockCount))
    # wind
    pg.draw.rect(screen, wind_color, (28 * blockFill, 22 * blockFill, 12 * blockFill, 1 * blockCount))
    pg.draw.rect(screen, wind_color, (35 * blockFill, 7 * blockFill, 3 * blockFill, 3 * blockCount))

    # 3
    pg.draw.rect(screen, wall_color, (5 * blockFill, 28 * blockFill, 14 * blockFill, 2 * blockCount))
    pg.draw.rect(screen, wall_color, (17 * blockFill, 30 * blockFill, 2 * blockFill, 16 * blockCount))
    pg.draw.rect(screen, wall_color, (5 * blockFill, 45 * blockFill, 14 * blockFill, 2 * blockCount))
    #pg.draw.rect(screen, wall_color, (5 * blockFill, 37 * blockFill, 12 * blockFill, 1 * blockCount))
    # lava
    pg.draw.rect(screen, lava_color, (10 * blockFill, 32 * blockFill, 2 * blockFill, 4 * blockCount))
    pg.draw.rect(screen, lava_color, (8 * blockFill, 48 * blockFill, 10 * blockFill, 1 * blockCount))
    # wind
    pg.draw.rect(screen, wind_color, (2 * blockFill, 29 * blockFill, 2 * blockFill, 17 * blockCount))

    # 4
    pg.draw.rect(screen, wall_color, (42 * blockFill, 28 * blockFill, 2 * blockFill, 19 * blockCount))
    pg.draw.rect(screen, wall_color, (31 * blockFill, 28 * blockFill, 2 * blockFill, 8 * blockCount))
    pg.draw.rect(screen, wall_color, (31 * blockFill, 36 * blockFill, 11 * blockFill, 2 * blockCount))
    # wind
    pg.draw.rect(screen, wind_color, (27 * blockFill, 39 * blockFill, 4 * blockFill, 8 * blockCount))
    pg.draw.rect(screen, wind_color, (35 * blockFill, 30 * blockFill, 4 * blockFill, 4 * blockCount))

    # make grid
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(screen, WHITE, rect, 1)

class Agent:
    '''the agent class '''
    def __init__(self, start_y, start_x, scr, animate):
        self.w = WIDTH//80
        self.h = WIDTH//80
        self.x = WIDTH//80 + WIDTH//160 - CENTER - self.w//2 + start_x * cellSize
        self.y = HEIGHT//80 + HEIGHT//160 - CENTER - self.h//2 + start_y * cellSize
        self.scr = scr
        self.my_rect = pg.Rect((self.x, self.y), (self.w, self.h))
        self.animate = animate

    def show(self, color):
        self.my_rect = pg.Rect((self.x,self.y), (self.w, self.h))
        pg.draw.rect(self.scr, color, self.my_rect)

    def wind(self):
        if self.animate is False:
            if matrix[int(self.y/cellSize)][int(self.x/cellSize)] == 1:
                windy = [-1, 0, 1]
                wind_val = np.random.choice(windy)

            else:
                wind_val = 0
        else:
            wind_val = 0

        return wind_val

    def hole(self):
        if self.animate is False:
            if matrix[int(self.y / cellSize)][int(self.x / cellSize)] == 4:
                return True
            else:
                return False
        else:
            return False

    def w_is_move_valid(self, a):
        '''checking for the validity of moves'''
        if 0 < self.x + a < WIDTH:
            return True
        else:
            return False

    def h_is_move_valid(self, a):
        '''checking for the validity of moves'''
        if 0 < self.y + a < HEIGHT:
            return True
        else:
            return False

    def w_move(self, a):
        '''move the agent'''
        if self.w_is_move_valid(a) and matrix[int(self.y/cellSize)][int((self.x+a)/cellSize)] != 2:
            pg.time.wait(TS)
            self.show(bg_color)
            wind_val = self.wind()
            hole = self.hole()

            if hole is True:
                self.x, self.y = 3, 3

            else:
                self.x += a + wind_val * cellSize
                if matrix[int(self.y/cellSize)][int(self.x/cellSize)] == 2 or self.x < 0 or self.x > 50*cellSize:
                    if a < 0:
                        self.x += cellSize
                    elif a > 0:
                        self.x -= cellSize

            self.show(agent_color)

    def h_move(self, a):
        '''move the agent'''
        if self.h_is_move_valid(a) and matrix[int((self.y+a)/cellSize)][int(self.x/cellSize)] != 2:
            pg.time.wait(TS)
            self.show(bg_color)
            wind_val = self.wind()
            hole = self.hole()

            if hole is True:
                self.x, self.y = 3, 3

            else:
                self.y += a + wind_val * cellSize
                if matrix[int(self.y / cellSize)][int(self.x / cellSize)] == 2 or self.y < 0 or self.y > 50*cellSize:
                    if a < 0:
                        self.y += cellSize
                    elif a > 0:
                        self.y -= cellSize

            self.show(agent_color)

def main():
    pg.init() # initialize pygame
    screen = pg.display.set_mode((WIDTH+2, HEIGHT+2))   # set up the screen
    pg.display.set_caption("Kevin Lu")              # add a caption
    bg = pg.Surface(screen.get_size())                  # get a background surface
    bg = bg.convert()
    bg.fill(bg_color)
    screen.blit(bg, (0,0))
    clock = pg.time.Clock()
    agent = Agent(0,0, screen, False)                               # instantiate an agent
    agent.show(agent_color)
    pg.display.flip()
    run = True
    while run:
        clock.tick(60)
        for event in pg.event.get():
            #print(agent.x, agent.y)
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                agent.w_move(cellSize)
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                agent.w_move(-cellSize)
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                agent.h_move(-cellSize)
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                agent.h_move(cellSize)

        screen.blit(bg, (0,0))
        draw_grid(screen)
        agent.show(agent_color)
        pg.display.flip()
        pg.display.update()
    pg.quit()


if __name__ == "__main__":
    main()