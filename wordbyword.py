# -*- coding: utf-8 -*-
import html
import os
import re

import tornado.web
from tornado.ncss import Server
from template_engine.parser import Parser
from database import story, word, user
import database

def get_current_user(response):
    username = response.get_secure_cookie('username')
    if username is None:
        return None
    return user.User.from_username(username.decode())

# Create the database
# database.create()
#   function:   stories()
#   arguments:  response
#   description:
#       When the page is called for listing the stories avaliable.
def stories(response):
    #list will contain:
    # title, burb and word count
    #stories = db.story_list()
    #require db.story_list_data()
    # arguments: no args
    # returns: title, short burb and word count
    stories = story.Story.story_list()
    #v = stories[0].first_word.add_child("word2")
    #print(v)
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

    username = response.get_secure_cookie('username')
    if not username:
        errors.append('You must be logged in to post a word')
        p = Parser.from_file("templates/createastory.html")
        variables = {'errors': errors }
        view = p.expand(variables)
        response.write(view)
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
        author = get_current_user(response)
        if author is None:
            errors.append('You must be logged in to post a word')
        if not errors:
            #write to the database
            new_story = story.Story(title, firstword, author)
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
    #   title=story.title,
    #   current="",#story.current,
    #   tree=render_word(story.first_word, title=True))
    # print("?", html)
    response.write(p.expand({"story": s, "errors":[]}))

def add_word(response, sid, wid):
    s = story.Story.from_id(sid)
    w = word.Word.from_id(wid)
    errors = []
    new_word = response.get_field("word").strip()
    #response.redirect("/story/" + str(s.story_id))
    if not new_word:
        errors.append("You didn't enter a word!")

    if " " in new_word:
        errors.append("Please only enter one word.")

    if len(new_word) > 20:
        errors.append("Your word is too long. Word must be below 21 characters long.")

    author = get_current_user(response)
    if author is None:
        errors.append('You must be logged in to post a word')
        
    if not errors: #if there are no errors
        w.add_child(new_word, author)
        response.redirect("/story/" + str(s.story_id))
        return

    errors.append("Please try again.")

    p = Parser.from_file("templates/viewstory.html")
    variables = {'errors': errors, "story": s}
    view = p.expand(variables)
    response.write(view)

def upvote(response, story_id, word_id):
    author = get_current_user(response)
    errors = []
    if author is None:
        errors.append('You must be logged in to post a word')
    if response.request.method == "POST" and not errors:
        #Write to databse
        w = word.Word.from_id(word_id)
        w.add_vote(author)
    response.redirect("/story/" + str(story_id))

def login(response):
        username = response.get_field('name')
        password = response.get_field('password')
        logged_name = response.get_secure_cookie('username')
        login_fail = False
        if logged_name is not None:
                username = logged_name.decode()
                print('logged in, user =', username)
        else:
                if user and password:
                        if user.User.login(username, password):
                                print('login success, user =', username)
                                response.set_secure_cookie('username', username)
                                response.redirect('/')
                                return
                        else:
                                login_fail = True
                                username = password = None
                else:
                        username = password = None
                
        p = Parser.from_file('templates/login.html')
        html = p.expand({ 'user' : username, 'login_fail' : login_fail })
        response.write(html)

def logout(response):
        response.clear_cookie('username')
        response.redirect('/login')

def register(response):
        logged_name = response.get_secure_cookie('username')
        if logged_name is None:
                username = response.get_field('name')
                password = response.get_field('password')
                print('user,pass =', username, password)
                if username and password is not None:
                        good_username = True if re.match(r'^\w+$', username) else False
                        username_taken = True if user.User.from_username(username) else False
                        good_password = (len(password) > 4)
                        print(good_username, good_password, username_taken)
                        if good_username and good_password and not username_taken:
                                response.set_secure_cookie('username', username)
                                user.User.create(username, password)
                                print(user, password)
                                response.redirect('/')
                                return
                        else:
                                username = password = None
                else:
                        username = password = None
                        good_username = good_password = True
                        username_taken = False
        else:
                response.redirect('/')
                return
                
        p = Parser.from_file('templates/register.html')
        html = p.expand({
                'user' : username,
                'good_username': good_username,
                'good_password': good_password,
                'username_taken': username_taken})
        response.write(html)

def profile(response, username):
        #get request, the list of stories they have made, list of stories they have contributed to maybe, last visit?, 
        display_user = user.User.from_username(username)
        
        p = Parser.from_file("templates/userProfile.html")
        variables = { "user":display_user}
        view = p.expand(variables)
        response.write(view)

if __name__ == "__main__":
    server = Server()
    server.register("/", stories)
    server.register("/style.css", style)
    server.register("/story", create)
    server.register("/story/(\d+)", view_story)
    server.register("/story/(\d+)/word/(\d+)/vote", upvote)
    server.register("/story/(\d+)/(\d+)/reply", add_word)
    server.register('/login', login)
    server.register('/logout', logout)
    server.register('/register', register)
    server.register('/user/(\w+)', profile)
    server.run()
