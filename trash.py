# Things we don't really need - just in case.
def index(response):
	response.write("Hello, World!<br>")
	for i in range(50):
		response.write("{0} ".format(str(i+1)))

def hello(response, name):
	response.write("Hello " + name.title())

server.register("/", index)
server.register("/hello/([a-z]+)", hello)