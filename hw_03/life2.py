import pygame
import random
from copy import deepcopy
from pygame.locals import *


class Cell:

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        if randomize:
            self.grid = [[Cell(i, j, bool(random.randint(0, 1))) for j in range(ncols)] for i in range(nrows)]
        else:
            self.grid = [[Cell(i, j) for j in range(ncols)] for i in range(nrows)]

    def get_neighbours(self, cell):
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i or j) and (0 <= cell.row + i < self.nrows) and (0 <= cell.col + j < self.ncols):
                    neighbours.append(self.grid[cell.row + i][cell.col + j])

        return neighbours

    def update(self):
        new_grid = deepcopy(self.grid)
        for cell in self:
            neighbours = self.get_neighbours(cell)
            count = sum(c.is_alive() for c in neighbours)
            if cell.is_alive():
                if count < 2 or count > 3:
                    new_grid[cell.row][cell.col].state = False
            else:
                if count == 3:
                    new_grid[cell.row][cell.col].state = True

        self.grid = new_grid
        return self

    @classmethod
    def from_file(cls, filename):
        grid = []
        with open(filename) as f:
            for row, line in enumerate(f):
                grid.append([Cell(row, col, bool(int(state))) for col, state in enumerate(line) if state in '01'])
        cell_list = cls(len(grid), len(grid[0]), False)
        cell_list.grid = grid
        return cell_list

    def __iter__(self):
        self.row_count, self.col_count = 0, 0
        return self

    def __next__(self):
        if self.row_count == self.nrows:
            raise StopIteration

        cell = self.grid[self.row_count][self.col_count]
        self.col_count += 1
        if self.col_count == self.ncols:
            self.col_count = 0
            self.row_count += 1

        return cell

    def __str__(self):
        str = ""
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.grid[row][col].is_alive():
                    str += "1 "
                else:
                    str += "0 "
            str += "\n"
        return str



class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Set window size
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Compute count of cells in horizontal and vertical directions
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Speed of the game
        self.speed = speed

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self):
        """
        Run the game
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Create cell list
        cell_list = CellList.from_file('pattern.txt')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Draw cell list
            self.draw_cell_list(cell_list)

            # One step in game - updating cells
            cell_list.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, cell_list: CellList):
        """
        Draw cells to surface
        """
        surface = self.screen
        size = self.cell_size

        for cell in cell_list:
            color = pygame.Color('green') if cell.is_alive() else pygame.Color('white')
            rect = [cell.col * size, cell.row * size, size, size]
            pygame.draw.rect(surface, color, rect)

        return self


if __name__ == '__main__':
	game = GameOfLife(500, 500, 25, 10)
	game.run()