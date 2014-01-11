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
