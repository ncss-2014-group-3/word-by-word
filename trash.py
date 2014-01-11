# Things we don't really need - just in case.
def index(response):
	response.write("Hello, World!<br>")
	for i in range(50):
		response.write("{0} ".format(str(i+1)))

def hello(response, name):
	response.write("Hello " + name.title())

def greet(response):
	first = response.get_field("fname", "John")
	last = response.get_field("lname", "Smith")
	response.write("Sup, {0} {1}.".format(first, last))

server.register("/", index)
server.register("/hello/([a-z]+)", hello)
server.register("/greet", greet)


##################
import random
class Word:
	def __init__(self):
		self._children = []
		self.children = lambda: self._children
		self.value = lambda: random.choice(["foo", "bar", "baz", "qux", "test"])
		self.id = lambda: random.randint(0, 50)

class Story:
	def __init__(self, w):
		self.title = lambda: "This is a test"
		self.first_word = lambda: w
		self.current = lambda: "Once upon a time"

w2 = Word()
w2._children = [
	Word(),
	Word(),
	Word()
]

w = Word()
w._children = [
	Word(),
	w2
]

s = Story(w)