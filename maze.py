from numpy.random import randint as rand


class Maze:
    def __init__(self):
        self.maze = {}
        self.maze_width = 81
        self.maze_height = 61
        self.corners = [(1, self.maze_height - 2), (self.maze_width - 2, self.maze_height - 2),
                        (self.maze_width - 2, 1)]

    def check_borders(self, x, y):
        if (x == 0 and (y >= 0 and y < self.maze_height) or
                y == 0 and (x >= 0 and x < self.maze_width) or
                x == self.maze_width - 1 and (y >= 0 and y < self.maze_height) or
                y == self.maze_height - 1 and (x >= 0 and x < self.maze_width)):
            return True
        else:
            return False

    def generate_maze(self, complexity=0.75, density=0.75):
        for x in range(0, self.maze_width):
            for y in range(0, self.maze_height):
                if self.check_borders(x, y):
                    self.maze[x, y] = 1
                else:
                    self.maze[x, y] = 0
        shape = ((self.maze_height // 2) * 2 + 1, (self.maze_width // 2) * 2 + 1)
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