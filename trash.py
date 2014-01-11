# Things we don't really need - just in case.
# def index(response):
# 	response.write("Hello, World!<br>")
# 	for i in range(50):
# 		response.write("{0} ".format(str(i+1)))

# def hello(response, name):
# 	response.write("Hello " + name.title())

# def greet(response):
# 	first = response.get_field("fname", "John")
# 	last = response.get_field("lname", "Smith")
# 	response.write("Sup, {0} {1}.".format(first, last))

# server.register("/", index)
# server.register("/hello/([a-z]+)", hello)
# server.register("/greet", greet)


##################
import random
class Word:
	def __init__(self, v, c=None):
		self._children = c if c is not None else []
		self.children = lambda: self._children
		self.value = lambda: v
		self.id = lambda: random.randint(0, 50)
	def __str__(self):
		return self.value()

class Story:
	def __init__(self, w):
		self.title = lambda: "This is a test"
		self.first_word = lambda: w
		self.current = lambda: "Once upon a time"

foo = Word("once", [
		Word("there", [
			Word("was", [
				Word("a", [
					Word("frog"),
					Word("douchebag")
				])
			])
		]),
		Word("upon", [
			Word("penis", [
				Word("land", [
					Word("needed")
				])
			]),
			Word("a", [
				Word("time", [
					Word("Tim", [
						Word("thought")
					]),
					Word("there", [
						Word("be", [
							Word("dragons")
						]),
						Word("was", [
							Word("a", [
								Word("cat"),
								Word("chicken")
							])
						])
					]),
				])
			])
		])
	])

s = Story(foo)

# w2 = Word()
# w2._children = [
# 	Word(),
# 	Word(),
# 	Word()
# ]

# w = Word()
# w._children = [
# 	Word(),
# 	w2
# ]

# s = Story(w)