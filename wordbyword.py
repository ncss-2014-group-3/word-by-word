# -*- coding: utf-8 -*-
import html
import textwrap

from tornado.ncss import Server

import template
import db

server = Server()

def render_word(word):
	children = word.children()
	if not children:
		html = """
		<div id="child-{cid}">
			{word}
		</div>
		""".format(cid=word.id(), word=str(word))
		return html
	else:
		children_html = (render_word(child) for child in children)
		html = """
		<div id="child-{cid}">
			{word}
			{children}
		</div>
		""".format(cid=word.id(), word=str(word), children="\n".join(children_html))
		return html

def story(response, sid):
	story = db.Story.from_id(sid)
	# title, words = db.story_from_id(sid)
	# current = "Once upon a time there was a swag-master called Alex"
	html = """
	<header id="something">
		<h1 id="main-title">{title}</h1>
		<h3 id="current-sentence">{current}</h3>
	</header>
	<content id="tree">
		{tree}
	</content>
	""".format(title=story.title(), current=story.current(), tree=render_word(story.first_word()))
	response.write(html)
	return html

if __name__ == "__main__":
	server.run()
