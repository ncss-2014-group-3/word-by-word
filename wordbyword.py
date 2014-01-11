# -*- coding: utf-8 -*-
import html

import tornado.web
from tornado.ncss import Server

from template_engine.parser import Parser
from database import story

import database
from database import story

# Create the database if it doesn't exist
if not os.path.isfile('database.db'):
  database.create()


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

    stories = story.Story.story_list()

    # story_list_data should return:
    #   titles and word count

    variables = {'stories': stories}

    #render the page from the template
    #create the parser object from template file
    p = Parser.from_file('templates/stories.html')
    #render the html code in var result
    result = p.expand(variables) # dict in expand
    #render the result to the client
    response.write(result)

def style(response):
	with open('style.css', 'r') as f:
		response.write(f.read())


def create(response):
    #get the variables we need using get_field
    title = response.get_field("title")
    firstword = response.get_field("firstword")
    # a list of strings of things that went wrong
    #we will give this to the template.
    errors = []
    if response.request.method == "POST":
        if not title:
            #we didn't get given a title
            errors.append("You didn't enter a title!")
        if len(title) > 50:
            errors.append("Your title was too long!")
        if not firstword:
            errors.append("You didn't enter a starting word!")
        if ' ' in firstword:
            errors.append("Please only enter one word.")
        if len(firstword) > 20:
            errors.append("Your word is too long. Word must be below 21 characters long.")

        if not errors:
            #write to the database
            new_story = story.Story(title, firstword)
            story_id = new_story.story_id
            response.redirect("/story/" + str(story_id))
            return

        #if there are errors, relay back to user
        errors.append("Please try again.")

    p = Parser.from_file("templates/createastory.html")
    variables = {'errors': errors }

    view = p.expand(variables)
    response.write(view)


def view_story(response, sid):
	s = story.Story.from_id(sid)

	if not s:
		raise tornado.web.HTTPError(404)

	p = Parser.from_file("templates/viewstory.html")

	# html = """
	# """.format(
	# 	title=story.title,
	# 	current="",#story.current,
	# 	tree=render_word(story.first_word, title=True))
	# print("?", html)
	response.write(p.expand({"story": s}))

if __name__ == "__main__":
	server = Server()
	server.register("/", stories)
	server.register("/style.css", style)
	server.register("/story", create)
	server.register("/story/(\d+)", view_story)
	server.run()
