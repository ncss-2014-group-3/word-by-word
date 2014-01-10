from tornado.ncss import Server
#import database
#db = Database
def index(response):
    response.write("Hello World! :) Welcome to SpyWare Exchange!")
    for x in range(100):
    	response.write(str(x) + '\n')

#	function:	stories()
#	arguments:	response
#	description:
#		When the page is called for listing the stories avaliable.
def stories(response):
	#stories = db.story_list()

	stories = ['The big bug','Harry Potter','The Green Sheep','The long snake','the small ant','the broken wheel']
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


server= Server()
server.register("/hello/([a-z]+)", hello)
server.register("/", stories)
server.register("/greet", greet)
server.run()
