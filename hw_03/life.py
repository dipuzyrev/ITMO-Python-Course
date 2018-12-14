import random
import pygame
from copy import copy, deepcopy
from pygame.locals import *


class GameOfLife:
	def __init__(self, width = 640, height = 480, cell_size = 10, speed = 10):
		self.width = width
		self.height = height
		self.cell_size = cell_size

		# Устанавливаем размер окна
		self.screen_size = width, height
		# Создание нового окна
		self.screen = pygame.display.set_mode(self.screen_size)
		
		# Вычисляем количество ячеек по вертикали и горизонтали
		self.cell_width = self.width // self.cell_size
		self.cell_height = self.height // self.cell_size
		
		# Скорость протекания игры
		self.speed = speed


	def run(self):
		pygame.init()
		clock = pygame.time.Clock()
		pygame.display.set_caption('Game of Life')
		self.screen.fill(pygame.Color('white'))
		running = True
		rects = self.cell_list(True)
		self.draw_cell_list(rects)
		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
			self.draw_grid()
			pygame.display.flip()
			rects = self.update_cell_list(rects)
			self.draw_cell_list(rects)
			clock.tick(self.speed)
		pygame.quit()


	def draw_grid(self):
		# http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
		for x in range(0, self.width, self.cell_size):
			pygame.draw.line(self.screen, pygame.Color('black'), 
				(x, 0), (x, self.height))
		for y in range(0, self.height, self.cell_size):
			pygame.draw.line(self.screen, pygame.Color('black'), 
				(0, y), (self.width, y))


	def cell_list(self, randomize = False):
		"""
		Создание списка клеток.

		Клетка считается живой, если ее значение равно 1. 
		В противном случае клетка считается мертвой, то 
		есть ее значение равно 0.
		Если параметр randomize = True, то создается список, где
		каждая клетка может быть равновероятно живой или мертвой.
		"""
		cells = []
		for row in range(self.cell_height):
			cells.append([])
			for col in range(self.cell_width):
				cells[row].append(random.randint(0,1) if randomize else 0)

		return cells


	def draw_cell_list(self, rects):
		"""
		Отображение списка клеток rects с закрашиванием их в 
		соответствующе цвета
		"""
		surface = self.screen
		size = self.cell_size

		for row in range(len(rects)):
			for col in range(len(rects[row])):
				color = pygame.Color('white') if rects[row][col] == 0 else pygame.Color('green')
				rect = [col * size, row * size, size, size]
				pygame.draw.rect(surface, color, rect)


	def get_neighbours(self, cell, cell_list):
		"""
		Вернуть список соседних клеток для клетки cell.

		Соседними считаются клетки по горизонтали,
		вертикали и диагоналям, то есть во всех
		направлениях.
		"""
		neighbours = []

		row = cell[0]
		col = cell[1]

		# print("Cell height: ", self.cell_height)
		# print("Cell width: ", self.cell_width)
		# print("cell: ", cell)

		if (row != 0) and (col != 0):
			neighbours.append(cell_list[row - 1][col - 1])
		if row != 0:
			neighbours.append(cell_list[row - 1][col])
		if (row != 0) and (col != (self.cell_width - 1)):
			neighbours.append(cell_list[row - 1][col + 1])
		if (col != (self.cell_width - 1)):
			neighbours.append(cell_list[row][col + 1])
		if (row != (self.cell_height - 1)) and (col != (self.cell_width - 1)):
			neighbours.append(cell_list[row + 1][col + 1])
		if (row != (self.cell_height - 1)):
			neighbours.append(cell_list[row + 1][col])
		if (row != (self.cell_height - 1)) and (col != 0):
			neighbours.append(cell_list[row + 1][col - 1])
		if (col != 0):
			neighbours.append(cell_list[row][col - 1])

		return neighbours


	def update_cell_list(self, cell_list):
		"""
		Обновление состояния клеток
		"""
		new_cell_list = self.get_deepcopy(cell_list)

		for row in range(len(cell_list)):
			for col in range(len(cell_list[row])):
				neighbours = self.get_neighbours((row, col), cell_list)
				if (cell_list[row][col] == 0):
					if neighbours.count(1) == 3:
						new_cell_list[row][col] = 1 # birth
				else:
					if (neighbours.count(1) < 2) or (neighbours.count(1) > 3):
						new_cell_list[row][col] = 0 # die

		return new_cell_list


	def get_deepcopy(self, list2d):
		new_list2d = []

		for row in range(len(list2d)):
			new_list2d.append(list2d[row].copy())

		return new_list2d


if __name__ == '__main__':
	game = GameOfLife(320, 240, 20)
	game.run()