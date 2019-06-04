import socket
import threading
from _thread import *

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
            # x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
            x = rand(0, self.window_width - 1 - 200)
            y = rand(0, self.window_height - 1)
            # if self.maze.maze[x, y] == 1:
            if self.maze.maze[x // 10, y // 10] == 1 \
                    or self.maze.maze[(x + 6) // 10, (y + 6) // 10] == 1 \
                    or self.maze.maze[(x + 6) // 10, y // 10] == 1 \
                    or self.maze.maze[x // 10, (y + 6) // 10] == 1:
                continue
            break
        return x, y

    def on_init(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Maze Game')

        self.font = pygame.font.SysFont('Arial', 24)
        self.text = self.font.render(self.name + "  " + str(self.seconds), True, (255, 0, 255))
        self.textRec = self.text.get_rect()
        self.textRec.center = (self.window_width - 100, self.window_height // 2 - 200)

        self.display_surface.fill((0, 0, 0))

        pygame.display.flip()

    def check_new_player(self, dic):
        return self.players.keys() == dic.keys()

    def add_new_player(self, x, y, color):
        pygame.draw.rect(self.display_surface, Color(color), Rect(x, y, 8, 8))
        pygame.display.flip()

    def on_render(self):
        # self.display_surface.fill((0, 0, 0))

        # for x in range(0, self.maze.maze_width):
        #    for y in range(0, self.maze.maze_height):
        #       if self.check_borders(x, y) == True:
        #          self.maze.maze[x, y] = 1
        #         pygame.draw.rect(self.display_surface, Color("Green"), Rect(x * 50, y * 50, 50, 50))
        #    else:
        #        self.maze.maze[x, y] = 0
        # print(players.keys())
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
        for player in self.players.keys():
            pygame.draw.rect(self.display_surface, Color(self.players[player][2]),
                             Rect(self.players[player][0], self.players[player][1], 8, 8))

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
        if len(self.points) < 10:
            self.generate_point()
        self.draw_points()
        pygame.display.flip()

    def blocked(self, maze, player):
        if self.players[player][0] < 0 or self.players[player][0] >= self.window_width - 200 or \
                self.players[player][1] < 0 or \
                self.players[player][1] >= self.window_height:
            return True
        if maze[self.players[player][0] // 10, self.players[player][1] // 10] == 1 \
                or maze[(self.players[player][0] + 6) // 10, (self.players[player][1] + 6) // 10] == 1 \
                or maze[(self.players[player][0] + 6) // 10, self.players[player][1] // 10] == 1 \
                or maze[self.players[player][0] // 10, (self.players[player][1] + 6) // 10] == 1:
            return True
        return False
    def generate_point(self):
        self.points.add(self.get_initpos())
    def draw_points(self):
        for point in self.points:
            pygame.draw.rect(self.display_surface, Color('blue'), Rect(point[0], point[1], 8, 8))
    def check_points(self):
        for player in self.players:
            print("s")

    # for i in range(0, 16):
    #    for j in range(0, 12):
    #       print(self.maze.maze[i, j], end=" ")
    #    print("\n")
