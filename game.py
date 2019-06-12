from pygame.locals import *
import pygame
from numpy.random import randint as rand
from maze import Maze


class Game:

    def __init__(self):
        self.maze = Maze()
        self.window_width = self.maze.maze_width * 10 + 200
        self.window_height = self.maze.maze_height * 10
        self.display_surface = None
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
        self.points = set()
        self.offset = 50

    def check_borders(self, x, y):
        if (x == 0 and (y >= 0 and y < self.maze.maze_height) or
                y == 0 and (x >= 0 and x < self.maze.maze_width) or
                x == self.maze.maze_width - 1 and (y >= 0 and y < self.maze.maze_height) or
                y == self.maze.maze_height - 1 and (x >= 0 and x < self.maze.maze_width)):
            return True
        else:
            return False

    def get_initpos(self):
        while True:
            x = rand(0, self.window_width - 1 - 200)
            y = rand(0, self.window_height - 1)
            # if self.maze.maze[x // 10, y // 10] == 1 \
            #         or self.maze.maze[(x + 6) // 10, (y + 6) // 10] == 1 \
            #         or self.maze.maze[(x + 6) // 10, y // 10] == 1 \
            #         or self.maze.maze[x // 10, (y + 6) // 10] == 1:
            if not self.blocked(self.maze.maze, x, y):
                break
        return x, y

    def on_init(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Maze Game')

        self.font = pygame.font.SysFont('Arial', 24)

        self.display_surface.fill((0, 0, 0))

        pygame.display.flip()

    def check_new_player(self, dic):
        return self.players.keys() == dic.keys()

    def add_new_player(self, x, y, color):
        pygame.draw.rect(self.display_surface, Color(color), Rect(x, y, 8, 8))
        pygame.display.flip()

    def on_render(self):
        for x in range(0, self.maze.maze_width):
            for y in range(0, self.maze.maze_height):
                if self.maze.maze[x, y] == 1:

                    pygame.draw.rect(self.display_surface, Color("Green"), Rect(x * 10, y * 10, 10, 10))
                else:
                    pygame.draw.rect(self.display_surface, Color("Black"), Rect(x * 10, y * 10, 10, 10))

        # if initial_position:
        for player in self.players.keys():
            pygame.draw.rect(self.display_surface, Color(self.players[player][2]),
                             Rect(self.players[player][0], self.players[player][1], 8, 8))

        self.font = pygame.font.SysFont('Arial', 24)
        pygame.draw.rect(self.display_surface, Color("Black"),
                         Rect(self.window_width - 190, 10, 180, self.window_height - 10))

        for player in self.players.keys():
            self.text = self.font.render(player + " scored " + str(self.players[player][3]) + "pts.", True,
                                         (255, 0, 255))
            self.textRec = self.text.get_rect()
            self.textRec.center = (self.window_width - 100, self.offset)

            self.display_surface.blit(self.text, self.textRec)
            self.offset += 50

        self.offset = 50
        if len(self.points) < 10:
            self.generate_point()
        self.check_points()
        self.draw_points()
        pygame.display.flip()

    def blocked(self, maze, x, y):
        if x < 0 or x >= self.window_width - 200 or \
                y < 0 or \
                y >= self.window_height:
            return True
        if maze[x // 10, y // 10] == 1 \
                or maze[(x + 6) // 10, (y + 6) // 10] == 1 \
                or maze[(x + 6) // 10, y // 10] == 1 \
                or maze[x // 10, (y + 6) // 10] == 1:
            return True
        for person in self.players.keys():
            if self.players[person][0] != x and self.players[person][1] != y and abs(
                    x - self.players[person][0]) < 8 and abs(y - self.players[person][1]) < 8:
                return True
        return False

    def generate_point(self):
        self.points.add(self.get_initpos())

    def draw_points(self):
        for point in self.points:
            pygame.draw.rect(self.display_surface, Color('blue'), Rect(point[0], point[1], 8, 8))

    def check_points(self):
        list_to_delete = list()
        for point in self.points:
            for player in self.players.keys():

                if self.players[player][0] in range(point[0] - 8, point[0] + 8) and self.players[player][1] in range(
                        point[1] - 8, point[1] + 8):
                    list_to_delete.append(point)
                    self.players[player][3] += 1
        for point in list_to_delete:
            self.points.remove(point)

    def getStartPoints(self):
        if len(self.players) == 0:
            return 0
        return int( sum([self.players[player][3] for player in self.players.keys()]) / len(self.players))
