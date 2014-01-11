<<<<<<< HEAD
# -*- coding: utf-8 -*-
import html
import textwrap

from tornado.ncss import Server

import template_engine
import db

# debugging
# from trash import s

def render_word(word, title=False):
	children = word.children()
	if children:
		children_html = '<td class="children">{}</td>'.format("\n".join(render_word(child) for child in children))
	else:
		# TODO: why won't this branch happen? :(
		children_html = ""
	tht = """
	<table id="child-{cid}" class="child">
		<tr>
			<td class="word">{word}</td>
			{children}
		</tr>
	</table>
	""".format(
		cid=int(word.id()),
		word=(html.escape(str(word).title())
			  if title
			  else html.escape(str(word))),
		children=children_html)
	return tht

def story(response, sid=1):
	# TODO: which do we want?
	# story = db.Story.from_id(sid)

	# TODO: REMOVE THIS COMPLETE AND UTTER TRASH
	with open("HTML/view_story.html") as f:
		x = f.read()

	story = s  # debugging
	html = """
	<header id="something">
		<h1 id="main-title">{title}</h1>
		<h3 id="current-sentence">{current}</h3>
	</header>
	<content id="story-tree">
		{tree}
	</content>
	""".format(title=story.title(), current=story.current(), tree=render_word(story.first_word(), title=True))
	# TODO: response.write(template.render("view_story.html", story=html))
	response.write(x.format(x=html))

if __name__ == "__main__":
	server = Server()
	server.register("/", story)
	server.run()
=======
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

    p = Parser.from_file("templates/createastory.html")
    variables = { 'title': title, 'firstword': firstword, 'errors': errors }
                  
    view = p.expand(variables)
    response.write(view)  
           
      

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
>>>>>>> origin/database
