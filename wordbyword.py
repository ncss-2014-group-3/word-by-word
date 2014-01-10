from tornado.ncss import Server
import database
db = Database
def index(response):
    response.write("Hello World! :) Welcome to SpyWare Exchange!")
    for x in range(100):
    	response.write(str(x) + '\n')

def hello(response, name):
	response.write("hello" + name)

def stories(response):
	# Var below returns a list of tuplets.
	# For each elemet of the list there is
	# a tuple for each story that is to be listed 
	stories = db.story_list()
	
	#debug = ['The big bug','Harry Potter','The Green Sheep','The long snake','the small ant','the broken wheel']
	# story_list_data should return: 
	#	titles

	#db.story_list_data()
	# arguments:
	# returns: 
	response.write("""
		<html>
		<head>
		</head>
		<body>

		""")
	for i in stories:
		response.write("<h1>")
		response.write(i)
		response.write("</h1>")
	response.write("""
		</body>
		</html>

		""")


	


def greet(response):
	fname = response.get_field("fname", "annomynous")
	lname = response.get_field("lname", "")
	response.write('''
<html>
<head>

</head>
<body>
<h1>list stories</h1>
<p>hello {fname} {lname}</p>
</body>
</html>
		'''.format(fname=fname, lname=lname))

server= Server()
server.register("/hello/([a-z]+)", hello)
server.register("/", stories)
server.register("/greet", greet)
server.run()
