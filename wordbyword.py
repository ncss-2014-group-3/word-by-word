# -*- coding: utf-8 -*-
import html
import textwrap

from tornado.ncss import Server

import template
import db

# debugging
from trash import w, s

server = Server()

def render_word(word):
	children = word.children()
	if not children:
		html = """
		<div id="child-{cid}" class="child">
			<span class="word">{word}</span>
		</div>
		""".format(cid=word.id(), word=str(word))
		return html
	else:
		children_html = (render_word(child) for child in children)
		html = """
		<div id="child-{cid}" class="child">
			<span class="word">{word}</span>
			<div class="children">{children}</div>
		</div>
		""".format(cid=word.id(), word=str(word), children="\n".join(children_html))
		return html

def story(response, sid):
	# TODO: which do we want?
	# story = db.Story.from_id(sid)
	story = s  # debugging
	html = """
	<header id="something">
		<h1 id="main-title">{title}</h1>
		<h3 id="current-sentence">{current}</h3>
	</header>
	<content id="story-tree">
		{tree}
	</content>
	""".format(title=story.title(), current=story.current(), tree=render_word(story.first_word()))
	# TODO: response.write(template.render("view_story.html", story=html))
	response.write(html)

if __name__ == "__main__":
	server.run()
