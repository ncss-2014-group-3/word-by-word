import re

TOKENS = re.compile(r'\{\{|\}\}|([^{}]|\{[^{]|\}[^}])*', re.DOTALL)


class Parser:
	def __init__(self, text):
		self._tokens = TOKENS.findall(text)
		self._length = len(tokens)
		self._upto = 0

	def end(self):
		return self._upto == self._length

	def peek(self):
		return None if self.end() else self._tokens[self._upto]

	def next(self):
		if not self.end():
			self._upto += 1

        
