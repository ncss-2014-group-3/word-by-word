# -*- coding: utf-8 -*-
import html

import tornado.web
from tornado.ncss import Server

from template_engine.parser import Parser
from database.story import Story

# def render_word(word, title=False):
# 	children = word.children
# 	if children:
# 		children_html = '<td class="children">{}</td>'.format("\n".join(render_word(child) for child in children))
# 	else:
# 		children_html = ""
# 	tht = """
# 	<table id="child-{cid}" class="child">
# 		<tr>
# 			<td class="word">{word}</td>
# 			{children}
# 		</tr>
# 	</table>
# 	""".format(
# 		cid=int(word.id),
# 		word=(html.escape(str(word.value)))
# 			  if title
# 			  else html.escape(str(word.value)),
# 		children=children_html)
# 	return tht

def view_story(response, sid):
	story = Story.from_id(sid)

	if not story:
		raise tornado.web.HTTPError(404)

	p = Parser.from_file("templates/viewstory.html")

	# html = """
	# """.format(
	# 	title=story.title,
	# 	current="",#story.current,
	# 	tree=render_word(story.first_word, title=True))
	# print("?", html)
	response.write(p.expand({"story": story}))

if __name__ == "__main__":
	server = Server()
	server.register("/story/(\d+)", view_story)
	server.run()