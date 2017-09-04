import collections, pygame


class FontHolder(collections.MutableMapping):
	"""A dictionary that holds fonts and automatically adds them if they are not already a part of the dictionary"""

	def __init__(self, *args, **kwargs):
		self._store = dict()
		self.update(dict(*args, **kwargs))  # use the free update to set keys
		pygame.font.init()

	def __getitem__(self, key):
		try:
			return self._store[self._keytransform(key)]
		except KeyError:
			self._store[self._keytransform(key)] = pygame.font.SysFont(key[0], key[1])
			return self._store[self._keytransform(key)]

	def __setitem__(self, key, value):
		raise TypeError("Don't set things in FontHolders!!!!")

	def __delitem__(self, key):
		del self._store[self._keytransform(key)]

	def __iter__(self):
		return iter(self._store)

	def __len__(self):
		return len(self._store)

	@staticmethod
	def _keytransform(key):
		"""
		Prevents keys that are not two tuples.
		:param key: key to check
		:return: key
		"""
		if len(key) != 2:
			raise KeyError("FontHolder requires a 2-tuple for keys")
		return key
