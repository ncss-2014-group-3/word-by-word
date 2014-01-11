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

	
	with open('head.html', 'r') as f:
		response.write(f.read())

	for title, blurb, count in stories:
		response.write("""
			<div class="story_list">
			<div class="title">{title}</div>
			<div class="blurb">{blurb}</div>
			<div class="count">{count}</div>
			</div>""".format(title=title, blurb=blurb, count=count))

	with open('foot.html', 'r') as f:
		response.write(f.read())


def style(response):
	with open('style.css', 'r') as f:
		response.write(f.read())
server= Server()
server.register("/", stories)
server.register("/style.css", style)
server.run()
