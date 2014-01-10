# -*- coding: utf-8 -*-
import html
import textwrap

from tornado.ncss import Server

import template
import db

server = Server()

def render_word(word):
	children = word.children()
	if len(children) == 0:
		html = """\
		<div id="child-{cid}">
			{word}
		</div>
		""".format(cid=word.id(), word=word.value())
		return html
	else:
		children_html = [render_word(child) for child in children]
		html = """\
		<div id="child-{cid}">
			{word}
			{children}
		</div>
		""".format(cid=word.id(), word=word.value(), children="\n".join(children_html))
		return html

def story(response, sid):
	story = db.Story.from_id(sid)
	# title, words = db.story_from_id(sid)
	# current = "Once upon a time there was a swag-master called Alex"
	html = """
	<!DOCTYPE html>
	<html>
	<head>
		<title>{title} - Word by Word</title>
	</head>
	<body>
		<h1>{title}</h1>
		<h3>{current}</h3>
		<p id="tree">
			{tree}
		</p>
	</body>
	</html>
	""".format(title=story.title(), current=story.current(), tree=render_word(story.first_word()))
	response.write(html)

if __name__ == "__main__":
	server.run()
