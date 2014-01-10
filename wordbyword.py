from tornado.ncss import Server
import db

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
	stories = db.get_all_stories()
	# story_list_data should return: 
	#	titles, authors, contents,
	#	short description, most popular
	#	unconfirmed word chain, last edited

	#db.story_list_data()
	# arguments:
	# returns: 






	response.write('''
<html>
<head>
<style>
body
{
	background-color: green;
}
h1
{
	color: white
}
</style>
</head>
<body>
<h1>list stories</h1>
<p>many stories here</p>
</body>
</html>
		''')


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
