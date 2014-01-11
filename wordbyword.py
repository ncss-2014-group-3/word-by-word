from tornado.ncss import Server
from template_engine.parser import Parser

                     
#import db
import re
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

def hello(response, name):
    response.write("Hello " + name + " ")

def create(response):
    invalid_word = False
    #get the variables we need using get_field
    title = response.get_field("title")
    firstword = response.get_field("firstword")
    # a list of strings of things that went wrong
    #we will give this to the template.
    errors = []
    if response.request.method == "POST":
        if title is None:
            #we didn't get given a title
            errors.append("You didn't enter a title!")
        if len(title) > 50:
            errors.append("Your title was too long!")
        if firstword is None:
            errors.append("You didn't enter a starting word!")  
        if ' ' in firstword:
            errors.append("Please only enter one word.")
        if errors:
            errors.append("Please try again.")

    p = Parser.from_file("HTML/createastory.html")
    variables = { 'title': title, 'firstword': firstword, 'errors': errors }
                  
    p.expand(variables)
        
       
 

    
    response.write("""
    <html>
    <head>
    <title> Create A Story </title>
    </head>


    <body>
    <strong>This is the create page</strong>
    </body>

    </html>
    """)


    

def greet(response):
    fname = response.get_field('fname', 'James')
    lname = response.get_field('lname', 'Curran')
    response.write("Hello " + fname + " " + lname + "!")

    
server = Server()
server.register("/", stories)
server.register("/style.css", style)
server.register("/hello/([a-z]+)", hello)
server.register("/story", create)
server.register("/greet", greet)
server.run()
