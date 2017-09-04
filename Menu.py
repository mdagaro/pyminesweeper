import pygame


class Button:
	"""
	Button to exist on the main menu. Does a function when clicked.
	"""
	def __init__(self,location,on_click=None,text='button',size=(100,30),buffer = (0,0)):
		"""
		Constructor
		:param location: where the button will appear on the screen
		:param on_click: what function the button will do when clicked
		:param text: the text displayed on the button
		:param size: the height and width of the button, default = (100,30)
		:param buffer: how much the text will be offset from the upper left corner
		"""
		if on_click is None:
			on_click = lambda: None
		self._click = on_click
		self.text = text
		self.location = self.x, self.y = location
		self.buffer = self.bufferx, self.buffery = buffer
		self.font_location = (self.x + self.bufferx, self.y + self.buffery)
		self.rect = pygame.Rect(location,size)

	def draw(self,screen,fonthandler):
		pygame.draw.rect(screen, pygame.Color('green'), self.rect)
		screen.blit(fonthandler[('consolas', 24)].render(self.text, True, pygame.Color('black')), self.font_location)

	def on_click(self):
		"""
		Does function when clicked with safeguards.
		"""
		try:
			self._click()
		except TypeError as err:
			print("Button.on_click must be a function\n{0}".format(err))
			raise


class Menu:
	"""
	A class to hold the buttons on the main menu screen.
	"""
	def __init__(self, buttons=()):
		"""
		Constructor
		:param buttons: the buttons to be added to the main menu screen
		"""
		self.visible = True
		self.buttons = buttons

	def draw(self, screen, fonts):
		"""
		Draws the main menu screen.
		:param screen: the screen to be drawn on
		:param fonts: a fonthandler for easy font access
		"""
		if self.visible:
			screen.fill(pygame.Color('black'))
			for b in self.buttons:
				b.draw(screen,fonts)
