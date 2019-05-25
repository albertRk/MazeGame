import pickle

from pygame.locals import *
import pygame
from numpy.random import randint as rand
from network import Network

n = Network()


class Game:

    def __init__(self):
        self.maze = Maze()
        self.window_width = self.maze.maze_width * 10 + 200
        self.window_height = self.maze.maze_height * 10
        self.display_surface = None
        self.player_x = 1
        self.player_y = 1
        self.speed = 2
        self.enems = {}
        self.not_to_draw = [False] * 5
        self.font = {}
        self.text = {}
        self.textRec = {}
        self.counter = 0
        self.seconds = 0
        self.name = ""
        self.players = dict()

    def check_borders(self, x, y):
        if (x == 0 and (y >= 0 and y < self.maze.maze_height) or
                y == 0 and (x >= 0 and x < self.maze.maze_width) or
                x == self.maze.maze_width - 1 and (y >= 0 and y < self.maze.maze_height) or
                y == self.maze.maze_height - 1 and (x >= 0 and x < self.maze.maze_width)):
            return True
        else:
            return False

    def get_initpos(self):
        shape = ((self.maze.maze_height // 2) * 2, (self.maze.maze_width // 2) * 2)
        while True:
            # x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
            x = rand(0, self.window_width - 1 - 200)
            y = rand(0, self.window_height - 1)
            # if self.maze.maze[x, y] == 1:
            if self.maze.maze[int(x / 10), int(y / 10)] == 1 \
                    or self.maze.maze[int((x + 8) / 10), int((y + 8) / 10)] == 1 \
                    or self.maze.maze[int((x + 8) / 10), int(y / 10)] == 1 \
                    or self.maze.maze[int(x / 10), int((y + 8) / 10)] == 1:
                continue
            break
        return x, y

    def on_init(self, maze):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Maze Game')

        self.font = pygame.font.SysFont('Arial', 24)
        self.text = self.font.render(self.name + "  " + str(self.seconds), True, (255, 0, 255))
        self.textRec = self.text.get_rect()
        self.textRec.center = (self.window_width - 100, self.window_height // 2 - 200)

        self.display_surface.fill((0, 0, 0))

        for x in range(0, self.maze.maze_width):
            for y in range(0, self.maze.maze_height):
                if self.check_borders(x, y) == True:
                    self.maze.maze[x, y] = 1
                    pygame.draw.rect(self.display_surface, Color("Green"), Rect(x * 10, y * 10, 10, 10))
                else:
                    self.maze.maze[x, y] = 0
        for i in range(0, 3):
            pygame.draw.rect(self.display_surface, Color("Blue"),
                             Rect([x[0] for x in self.maze.corners][i] * 10,
                                  [x[1] for x in self.maze.corners][i] * 10, 10, 10))
        #

        self.maze.maze = maze
        # self.maze.generate_maze()
        # print(maze.keys())
        for x in range(0, self.maze.maze_width):
            for y in range(0, self.maze.maze_height):
                if self.maze.maze[x, y] == 1:
                    pygame.draw.rect(self.display_surface, Color("Green"), Rect(x * 10, y * 10, 10, 10))

        (initx, inity) = self.get_initpos()
        pygame.draw.rect(self.display_surface, Color("Red"), Rect(initx, inity, 8, 8))
        self.player_x = initx
        self.player_y = inity

        k = 0

        while k != 5:
            (ex, ey) = self.get_initpos()
            if ex != self.player_x and ey != self.player_y:
                self.enems[k] = (ex, ey)
                k += 1
                pygame.draw.rect(self.display_surface, Color("Blue"), Rect(ex, ey, 8, 8))

        pygame.display.flip()

    def check_new_player(self, dic):
        return self.players.keys() == dic.keys()

    def add_new_player(self, x, y):
        pygame.draw.rect(self.display_surface, Color("Red"), Rect(x, y, 8, 8))
        pygame.display.flip()

    def on_render(self, dic):
        # self.display_surface.fill((0, 0, 0))

        # for x in range(0, self.maze.maze_width):
        #    for y in range(0, self.maze.maze_height):
        #       if self.check_borders(x, y) == True:
        #          self.maze.maze[x, y] = 1
        #         pygame.draw.rect(self.display_surface, Color("Green"), Rect(x * 50, y * 50, 50, 50))
        #    else:
        #        self.maze.maze[x, y] = 0

        for x in range(0, self.maze.maze_width):
            for y in range(0, self.maze.maze_height):
                if self.maze.maze[x, y] == 1:

                    pygame.draw.rect(self.display_surface, Color("Green"), Rect(x * 10, y * 10, 10, 10))
                else:
                    pygame.draw.rect(self.display_surface, Color("Black"), Rect(x * 10, y * 10, 10, 10))

        for i in range(0, 3):
            pygame.draw.rect(self.display_surface, Color("Blue"),
                             Rect([x[0] for x in self.maze.corners][i] * 10,
                                  [x[1] for x in self.maze.corners][i] * 10, 10, 10))

        # if initial_position:
        for player in dic.keys():
            pygame.draw.rect(self.display_surface, Color("Red"), Rect(dic[player][0], dic[player][1], 8, 8))
        for k in range(0, 5):
            if self.not_to_draw[k] == False and self.player_x >= self.enems[k][0] - 2 and self.player_x <= \
                    self.enems[k][0] + 10 \
                    and self.player_y >= self.enems[k][1] - 2 and self.player_y <= self.enems[k][1] + 10:
                pygame.draw.rect(self.display_surface, Color("Black"), Rect(self.enems[k][0], self.enems[k][1], 8, 8))
                self.not_to_draw[k] = True
            elif self.not_to_draw[k] == False:
                pygame.draw.rect(self.display_surface, Color("Blue"), Rect(self.enems[k][0], self.enems[k][1], 8, 8))

        # else:
        # pygame.draw.rect(self.display_surface, Color("Red"), Rect(self.player_x*10, self.player_y*10, 8, 8))

        self.display_surface.blit(self.text, self.textRec)
        self.counter += 1
        if self.counter == 45:
            self.counter = 0
            self.seconds += 1
            pygame.draw.rect(self.display_surface, Color("Black"),
                             Rect(self.window_width - 190, 10, 180, self.window_height - 10))
            self.text = self.font.render(self.name + "  " + str(self.seconds), True, (255, 0, 255))
            self.textRec = self.text.get_rect()
            self.textRec.center = (self.window_width - 100, self.window_height // 2 - 200)

        pygame.display.flip()

        # for i in range(0, 16):
        #    for j in range(0, 12):
        #       print(self.maze.maze[i, j], end=" ")
        #    print("\n")

    def blocked(self):
        if self.player_x < 0 or self.player_x >= self.window_width - 200 or self.player_y < 0 or self.player_y >= self.window_height:
            return True
        if self.maze.maze[int(self.player_x / 10), int(self.player_y / 10)] == 1 \
                or self.maze.maze[int((self.player_x + 6) / 10), int((self.player_y + 6) / 10)] == 1 \
                or self.maze.maze[int((self.player_x + 6) / 10), int(self.player_y / 10)] == 1 \
                or self.maze.maze[int(self.player_x / 10), int((self.player_y + 6) / 10)] == 1:
            return True
        return False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            theApp.move_right()

            # initial_position = True

        if keys[K_LEFT]:
            theApp.move_left()

            # initial_position = True

        if keys[K_UP]:
            theApp.move_up()

            # initial_position = True

        if keys[K_DOWN]:
            theApp.move_down()

            # initial_position = True

        if keys[K_ESCAPE]:
            running = False

    def move_right(self):
        self.player_x = self.player_x + 2 * self.speed
        if self.blocked():
            self.player_x = self.player_x - 2 * self.speed

    def move_left(self):
        self.player_x = self.player_x - 2 * self.speed
        if self.blocked():
            self.player_x = self.player_x + 2 * self.speed

    def move_up(self):
        self.player_y = self.player_y - 2 * self.speed
        if self.blocked():
            self.player_y = self.player_y + 2 * self.speed

    def move_down(self):
        self.player_y = self.player_y + 2 * self.speed
        if self.blocked():
            self.player_y = self.player_y - 2 * self.speed


class Maze:

    def __init__(self):
        self.maze = {}
        self.maze_width = 80
        self.maze_height = 60
        self.corners = [(1, self.maze_height - 2), (self.maze_width - 2, self.maze_height - 2),
                        (self.maze_width - 2, 1)]

    def generate_maze(self, complexity=0.75, density=0.75):
        shape = ((self.maze_height // 2) * 2, (self.maze_width // 2) * 2)
        complexity = int(complexity * (5 * (shape[0] + shape[1])))
        density = int(density * ((shape[0] // 2) * (shape[1] // 2)))

        for i in range(density):
            x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
            self.maze[x, y] = 1
            for j in range(complexity):
                neighbours = []
                if x > 1: neighbours.append((x - 2, y))
                if x < shape[1] - 2: neighbours.append((x + 2, y))
                if y > 1: neighbours.append((x, y - 2))
                if y < shape[0] - 2: neighbours.append((x, y + 2))
                if len(neighbours):
                    temp = neighbours[rand(0, len(neighbours) - 1)]
                    x1 = temp[0]
                    y1 = temp[1]
                    # print(x1, y1)
                    if self.maze[x1, y1] == 0:
                        self.maze[x1, y1] = 1
                        self.maze[x1 + (x - x1) // 2, y1 + (y - y1) // 2] = 1
                        x, y = x1, y1


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def convert_maze(maze):
    result = dict()
    for key in maze.keys():
        cords = key.split(',')
        result[int(cords[0]), int(cords[1])] = maze[key]
    return result


if __name__ == "__main__":
    theApp = Game()
    # playerNumber = n.senddata(str(theApp.player_x) + "," + str(theApp.player_y))
    theApp.players[n.getPlayerNumber()] = (theApp.player_x, theApp.player_y)
    theApp.players[0] = (theApp.player_x, theApp.player_y)
    maze = convert_maze(n.getMaze())
    print(len(maze))
    # theApp.maze.maze = maze

    theApp.on_init(maze)
    running = True
    theApp.name = ""
    # initial_position = False
    while running:
        pygame.event.pump()
        dic = n.senddata(str(theApp.player_x) + "," + str(theApp.player_y))
        if theApp.check_new_player(dic):
            for key in dic.keys():
                if key not in theApp.players:
                    theApp.add_new_player(dic[key][0], dic[key][1])
                    theApp.players[key] = dic[key]
        for ev in pygame.event.get():
            if ev.type == KEYDOWN:
                if ev.unicode.isalpha():
                    theApp.name += ev.unicode
        theApp.move()
        theApp.on_render(dic)

    pygame.quit()
