import pygame
from Menu import Menu, Button
from Font_holder import FontHolder
from GameScreen import GameScreen
import copy


class App:
	"""
	The minesweeper game app. Has two main screens, a menu screen, and a game screen.
	"""
	def __init__(self):
		"""
		Constructor
		"""
		self.size = self.width, self.height = int(640*1.5), int(400*1.5)
		self._display_surf = None
		self._running = True
		self.font_holder = FontHolder()
		self._init_gamescreen()
		self.queue = []

	def _init_gamescreen(self):
		self.game = GameScreen(19, 11, 5)
		def back():
			self.menu.visible = True
			self.game.visible = False
			self.game.reset()
		def reset():
			self.game.tiles = self.game.init_tiles(self.game.transform)
		back_button = Button((50,10),on_click=back,text="return")
		reset_button = Button((300,10),on_click=reset,text="reset")
		self.game.buttons = (back_button,reset_button)


	def init_menu(self):
		"""
		Sets up the menu and its buttons.
		"""
		self.menu = Menu()

		def open_game():
			self.game.visible = True
			self.menu.visible = False
		def easy():
			self.game.width=8
			self.game.height=8
			self.game.num_bombs = 10
			self.game.tiles = self.game.init_tiles(self.game.transform)
			open_game()
		def medium():
			self.game.width = 16
			self.game.height = 16
			self.game.num_bombs = 40
			self.game.tiles = self.game.init_tiles(self.game.transform)
			open_game()
		def hard():
			self.game.width = 24
			self.game.height = 24
			self.game.num_bombs = 99
			self.game.tiles = self.game.init_tiles(self.game.transform)
			open_game()
		easy_button = Button((50, 55), on_click=easy, buffer=(10, 2))
		medium_button = Button((50, 55*2), on_click=medium, buffer=(10, 2))
		hard_button = Button((50, 55*3), on_click=hard, buffer=(10, 2))
		self.menu.buttons = (easy_button,medium_button,hard_button)

	def on_init(self):
		"""
		Initializes pygame and font handler, and sets up the surface and main menu.
		"""
		pygame.init()
		pygame.font.init()

		self._display_surf = pygame.display.set_mode(self.size,pygame.HWSURFACE)
		self._display_surf.fill(pygame.Color('black'))
		self._running = True

		self.init_menu()

	def on_event(self, event):
		"""
		Handles events thrown by pygame.
		:param event: event to handle
		"""
		if event.type == pygame.QUIT:
			self._running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouse_pos = pygame.mouse.get_pos()
				if self.menu.visible:
					for b in self.menu.buttons:
						if b.rect.collidepoint(mouse_pos):
							b.on_click()
				elif self.game.visible:
					for column in self.game.tiles:
						for tile in column:
							if tile.rect.collidepoint(mouse_pos) and not tile.is_flagged:
								self.game.cascade(tile)
					for b in self.game.buttons:
						if b.rect.collidepoint(mouse_pos):
							b.on_click()
			elif event.button == 3:
				mouse_pos = pygame.mouse.get_pos()
				if self.game.visible:
					for column in self.game.tiles:
						for tile in column:
							if tile.rect.collidepoint(mouse_pos):
								tile.is_flagged = not tile.is_flagged
			elif event.button == 4:
				self._display_surf.scroll(0,-1)
			elif event.button == 5:
				self._display_surf.scroll(0,5)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				mouse_pos = pygame.mouse.get_pos()
				if self.game.visible:
					for column in self.game.tiles:
						for tile in column:
							if tile.rect.collidepoint(mouse_pos):
								tile.is_flagged = not tile.is_flagged

	def on_loop(self):
		"""
		Checks whether you've won the game.
		:return:
		"""
		# TODO set up loop

	def on_render(self):
		"""
		Draws the menu or the main game screen.
		"""
		self.menu.draw(self._display_surf, self.font_holder)
		self.game.draw(self._display_surf, self.font_holder)
		pygame.display.flip()

	def on_cleanup(self):
		"""
		Quits pygame.
		"""
		pygame.quit()

	def on_execute(self):
		"""
		Runs the game.
		"""
		self.on_init()
		while self._running:
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()

if __name__ == "__main__":
	theApp = App()
	theApp.on_execute()
