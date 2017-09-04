from Tile import MyTile
import random
import pygame


class GameScreen:
	"""
	Screen handler for the actual minesweeper game. Holds the tiles in the game along with their properties, and draws
	the game out.
	"""

	def __init__(self,width,height,num_bombs,buttons=(),transform=0.5):
		"""
		Constructor
		:param width: number of tiles wide the game is
		:param height: number of tiles high the game is
		:param num_bombs: number of bombs the game has
		"""
		self.size  = self.width, self.height = width, height
		self.num_bombs = num_bombs
		self.transform = transform
		self.tiles = self.init_tiles(transform)
		print(self.tiles)
		self.visible = False
		self.buttons = buttons

	def init_tiles(self,transform):
		"""
		Generates the tiles for the game. Transforms the size of the tiles depending on how many rows there are.
		:param transform: degree to with the dransform the tiles
		:return: a tuple matrix containing all the tiles
		"""
		tiles = []
		bomb_locations = []

		while len(bomb_locations) < self.num_bombs:
			matrix = (random.randint(0,self.width-1),random.randint(0,self.height-1))
			if matrix not in bomb_locations:
				bomb_locations.append(matrix)
		for i in range(self.width):
			column = []
			for j in range(self.height):
				bomb = False
				if (i,j) in bomb_locations:
					bomb = True
				location = (50*transform*i+50,50*transform*j+50)
				matrix = (i,j)
				column.append(MyTile(location, bomb, transform, matrix))
			tiles.append(column)
		return tuple(tuple(x) for x in tiles)



	def get_surrounding_tiles(self, starting_tile):
		x, y = starting_tile.matrix
		adjacent = []
		starting_tile.reveal(self)
		try:
			if x == 0 or y == 0:
				raise IndexError
			adjacent.append(self.tiles[x - 1][y - 1])
		except IndexError:
			pass
		try:
			if x == 0:
				raise IndexError
			adjacent.append(self.tiles[x - 1][y])
		except IndexError:
			pass
		try:
			if x == 0:
				raise IndexError
			adjacent.append(self.tiles[x - 1][y + 1])
		except IndexError:
			pass
		try:
			if y == 0:
				raise IndexError
			adjacent.append(self.tiles[x + 1][y - 1])
		except IndexError:
			pass
		try:
			adjacent.append(self.tiles[x + 1][y])
		except IndexError:
			pass
		try:
			adjacent.append(self.tiles[x + 1][y+1])
		except IndexError:
			pass
		try:
			if y == 0:
				raise IndexError
			adjacent.append(self.tiles[x][y-1])
		except IndexError:
			pass
		try:
			adjacent.append(self.tiles[x][y+1])
		except IndexError:
			pass
		return adjacent

	def _is_marked_tile(self,tile):
		return tile.get_bomb_num(self) == 0

	def num_surrounding_mines(self,tile):
		"""
		Finds the number of bombs surrounding a tile
		:param tile: the tile being looked at
		:return: the number of bombs surrounding that tile
		"""
		x,y = tile.matrix
		num = 0
		try:
			if x == 0 or y == 0:
				raise IndexError
			num += self.is_bomb(self.tiles[x - 1][y - 1])
		except IndexError:
			num += 0
		try:
			if x == 0:
				raise IndexError
			num += self.is_bomb(self.tiles[x - 1][y])
		except IndexError:
			num += 0
		try:
			if x == 0:
				raise  IndexError
			num += self.is_bomb(self.tiles[x - 1][y + 1])
		except IndexError:
			num += 0
		try:
			if y == 0:
				raise IndexError
			num += self.is_bomb(self.tiles[x+1][y - 1])
		except IndexError:
			num += 0
		try:
			num += self.is_bomb(self.tiles[x+1][y])
		except IndexError:
			num += 0
		try:
			num += self.is_bomb(self.tiles[x+1][y + 1])
		except IndexError:
			num += 0
		try:
			if y == 0:
				raise IndexError
			num += self.is_bomb(self.tiles[x][y - 1])
		except IndexError:
			num += 0
		try:
			num += self.is_bomb(self.tiles[x][y + 1])
		except IndexError:
			num += 0
		return num

	@staticmethod
	def is_bomb(tile):
		"""
		Checkes if tile is a bomb
		:param tile: the tile to be check
		:return: 1 if its a bomb, zero if not
		"""
		return 1 if tile.is_bomb else 0

	def draw(self, screen, fonthandler):
		"""
		Draws the tiles onto the screen.
		:param screen: the screen to draw the tiles on
		:param fonthandler: handles the fonts for easy access in drawing
		"""
		if self.visible:
			screen.fill(pygame.Color('white'))
			for column in self.tiles:
				for t in column:
					t.draw(screen, fonthandler)
			for b in self.buttons:
				b.draw(screen,fonthandler)
			if self.is_solved():
				print("winner")
				screen.blit(
					fonthandler[('arial', 72)].render("You Win!", True, pygame.Color('black')), (400, 50))

	def is_solved(self):
		return all(all(t.revealed for t in column if not t.is_bomb) for column in self.tiles)

	def reset(self):
		self.width = None
		self.height = None
		self.tiles = ()
