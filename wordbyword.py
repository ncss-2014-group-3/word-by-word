# -*- coding: utf-8 -*-
import html

from tornado.ncss import Server

import template
import db

server = Server()

def greet(response):
	first = response.get_field("fname", "John")
	last = response.get_field("lname", "Smith")
	response.write("Sup, {0} {1}.".format(first, last))

def story(response, sid):
	title, words = db.story_from_id(sid)
	# current = ???
	current = "Once upon a time there was a swag-master called Alex"
	html = """
	<!DOCTYPE html>
	<html>
	<head>
		<title>{title} - Word by Word</title>
	</head>
	<body>
		<h1>{title}</h1>
		<h3>{current}</h3>
		<p>
			<b>story tree goes here</b>
		</p>
	</body>
	</html>
	""".format(title=title, current=current)
	response.write(html)

server.register("/greet", greet)
server.run()
