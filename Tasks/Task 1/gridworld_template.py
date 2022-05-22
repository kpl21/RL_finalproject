import numpy as np
import pygame as pg

#Constants
WIDTH = 600     # width of the environment (px)
HEIGHT = 600    # height of the environment (px)
CENTER = 15
#START_Y, START_X = 0,0
TS = 10         # delay in msec
NC = 20          # number of cells in the environment
cellSize = WIDTH // NC

# define colors
goal_color = pg.Color(0, 100, 0)
start_color = pg.Color(100, 0, 0)
bg_color = pg.Color(0, 0, 0)
wall_color = pg.Color(225, 217, 209)
lava_color = pg.Color(255, 69, 0)
wind_color = pg.Color(50, 205, 50)
hole_color = pg.Color(105, 105, 105)
teleport_color = pg.Color(0, 0, 204)

line_color = pg.Color(128, 128, 128)
agent_color = pg.Color(120,120,0)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

matrix = np.zeros((20,20), int)

wind = [(1,6), (1,7), (1,8), (2,6), (2,7), (2,8), (8,5), (8,6),
        (9,5), (9,6), (10,5), (10,6), (11,5), (11,6), (12,5), (12,6), (13,5), (13,6)]

wall = [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (7,12), (8,12), (9,12), (10,12),
        (11,12), (12,12), (13,12), (14,12), (15,12)]

lava = [(0,12), (0,13), (0,14), (0,15), (0,16), (0,17), (0,18),
        (1,12), (1,13), (1,14), (1,15), (1,16), (1,17), (1,18),
        (2,12), (2,13), (2,14), (2,15), (2,16), (2,17), (2,18),
        (3,12), (3,13), (3,14), (3,15), (3,16), (3,17), (3,18)]

hole = [(17,3), (17,4), (18,3), (18,4), (14,16), (14,17), (14,18), (15,16), (15,17), (15,18),
        (16,16), (16,17), (16,18)]

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
    blockSize = 30
    blockFill = WIDTH // NC
    blockCount = HEIGHT/20
    '''a function to draw gridlines and other objects'''
    # draw goal state
    pg.draw.rect(screen, goal_color, (WIDTH - blockFill, WIDTH - blockFill , blockFill, blockCount))
    # draw start state
    pg.draw.rect(screen, start_color, (0, 0, blockFill, blockCount))
    # draw wall state
    pg.draw.rect(screen, wall_color, (4 * blockFill, 0, blockFill, 7 * blockCount))
    pg.draw.rect(screen, wall_color, (7 * blockFill, 12 * blockFill, 9 * blockFill, blockCount))
    # draw lava state
    pg.draw.rect(screen, lava_color, (0, 12*blockFill, 4 * blockFill, 7 * blockCount))
    # draw wind state
    pg.draw.rect(screen, wind_color, (blockFill, 6 * blockFill, 2 * blockFill, 3 * blockCount))
    pg.draw.rect(screen, wind_color, (8 * blockFill, 5 * blockFill, 6 * blockFill, 2 * blockCount))
    # draw hole state
    pg.draw.rect(screen, hole_color, (17 * blockFill, 3 * blockFill, 2 * blockFill, 2 * blockCount))
    pg.draw.rect(screen, hole_color, (14 * blockFill, 16 * blockFill, 3 * blockFill, 3 * blockCount))

    # make grid
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(screen, WHITE, rect, 1)

class Agent:
    '''the agent class '''
    def __init__(self, start_y, start_x, scr, animate):
        self.w = WIDTH//30
        self.h = WIDTH//30
        self.x = WIDTH//30 + WIDTH//60 - CENTER - self.w//2 + start_x * cellSize
        self.y = HEIGHT//30 + HEIGHT//60 - CENTER - self.h//2 + start_y * cellSize
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
                self.x, self.y = 5, 5

            else:
                self.x += a + wind_val * cellSize
                if matrix[int(self.y/cellSize)][int(self.x/cellSize)] == 2 or self.x < 0 or self.x > 20*cellSize:
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
                self.y, self.x = 5, 5

            else:
                self.y += a + wind_val * cellSize
                if matrix[int(self.y / cellSize)][int(self.x / cellSize)] == 2 or self.y < 0 or self.y > 20*cellSize:
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
    agent = Agent(0,0,screen, False)                               # instantiate an agent
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