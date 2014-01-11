from tornado.ncss import Server
from template_engine.parser import Parser
#import database
#db = Database

#	function:	stories()
#	arguments:	response
#	description:
#		When the page is called for listing the stories avaliable.
def stories(response):
	#list will contain:
	# title, burb and word count
	#stories = db.story_list()

	#require db.story_list_data()
	# arguments: no args
	# returns: title, short burb and word count



	stories = [
	("The big bug","big bug wanted a big hug",1002),
	("Harry Potter","the boy who lived",5000),
	("The Green Sheep","thomas's bedtime story",1450),
	("The long snake","pun on python coding",6354),
	("the small ant","got squashed",3),
	("the broken wheel","went round and round and fell down",789),
	]
	# story_list_data should return: 
	#	titles

	#render the page from the template
	#create the parser object from template file
	p = Parser.from_file('templates/list-of-stories.html')
	#render the html code in var result
	result = p.expand({'stories': []})
	#render the result to the client
	response.write(result)

def style(response):
	with open('style.css', 'r') as f:
		response.write(f.read())
server= Server()
server.register("/", stories)
server.register("/style.css", style)
server.run()
