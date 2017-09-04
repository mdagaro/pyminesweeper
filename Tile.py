import pygame


class Tile:
	"""
	Basic class for the tiles that fill up the minesweeper game.
	"""
	def __init__(self,start_image,reveal_image_normal, reveal_image_bomb, flagged_image, location, is_bomb):
		"""
		Constructor
		:param start_image: the image that the tile will appear when not revealed
		:param reveal_image_normal: the image that will appear when the tile is revealed and not a bomb
		:param reveal_image_bomb: the image that will appear if the tile is a bomb
		:param location: the location the tile will appear at
		:param is_bomb: whether or not the tile is a bomb
		"""
		self.location = self.x, self.y = location
		self.is_bomb = is_bomb
		self.revealed = False
		self.rect = pygame.Rect(location,(50,50))
		self._start_img = start_image
		if self.is_bomb:
			self._reveal_img = reveal_image_bomb
		else:
			self._reveal_img = reveal_image_normal
		self._flagged_image = flagged_image
		self.is_flagged = False
		self.bomb_num = None


	def draw(self,screen,fonthandler, buffer=(8,0)):
		"""
		Draws the tile to the screen.
		:param screen: the screen to be drawn on
		:param fonthandler: the font handler
		:param buffer: amount to buffer the position of the number
		"""
		if self.revealed:
			screen.blit(self._reveal_img,self.location)
			if not self.is_bomb:
				position = (self.x + buffer[0], self.y + buffer[1])
				if self.bomb_num != 0:
					screen.blit(fonthandler[('georgia', 18)].render(str(self.bomb_num), True, pygame.Color('black')),
						position)
		elif self.is_flagged:
			screen.blit(self._flagged_image, self.location)
		else:
			screen.blit(self._start_img,self.location)

	def get_bomb_num(self,tiles):
		if self.bomb_num is None:
			self.bomb_num = tiles.num_surrounding_mines(self)
		return self.bomb_num

	def reveal(self,tiles):
		self.revealed = True
		self.bomb_num = tiles.num_surrounding_mines(self)

	def __str__(self):
		"""Converts to string"""
		return '({}.{})'.format(self.matrix[0],self.matrix[1],self.is_bomb)

	def __repr__(self):
		return "Tile({},{},{})".format(self.matrix[0],self.matrix[1],self.is_bomb)

class MyTile(Tile):
	"""
	A supset of Tile for ease of writing.
	"""
	def __init__(self,location,is_bomb,transform,matrix):
		"""
		Constructor
		:param location: where the tile will be placed
		:param is_bomb: whether or not the tile is a bomb
		:param transform: what degree to transform the tile to
		:param matrix: where in the tile matrix the tile is
		"""
		trans = (int(transform*50),int(transform*50))
		unrevealed = pygame.transform.smoothscale(pygame.image.load('./resources/tile.png'), trans)
		bomb = pygame.transform.smoothscale(pygame.image.load('./resources/mine.png'), trans)
		notbomb = pygame.transform.smoothscale(pygame.image.load('./resources/selected_tile.png'), trans)
		flagged = pygame.transform.smoothscale(pygame.image.load('./resources/flagged.png'), trans)
		Tile.__init__(self, unrevealed, notbomb, bomb, flagged, location, is_bomb)
		self.rect = pygame.Rect(location,trans)
		self.matrix = matrix

