# -*- coding: utf-8 -*-
import re

import tornado.web
from tornado.ncss import Server
from template_engine.parser import render
from database import story, word, user

EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$')


def get_current_user(response):
    username = response.get_secure_cookie('username')

    if username is None:
        return None

    return user.User.from_username(username.decode())


def render_stories(response, stories):
    variables = {
        'stories': stories,
        'user': get_current_user(response)
    }

    response.write(render(
        'templates/stories.html',
        variables
    ))


def stories(response):
    """
    function:   stories()
    arguments:  response
    description:
        When the page is called for listing the stories avaliable.
    """
    render_stories(
        response,
        story.Story.story_list()
    )


def my_stories(response):
    username = get_current_user(response)
    if username is None:
        response.redirect("/")

    else:
        render_stories(
            response,
            username.own_stories
        )


def style(response):
    with open('style.css', 'r') as f:
        response.write(f.read())


def create(response):
    # get the variables we need using get_field
    title = response.get_field("title")
    firstword = response.get_field("firstword")
    # a list of strings of things that went wrong
    # we will give this to the template.
    errors = []

    username = response.get_secure_cookie('username')
    if not username:
        errors.append('You must be logged in to post a story')
        variables = {'errors': errors, 'user': get_current_user(response)}

        return render(
            "templates/createastory.html",
            variables,
        )

    if response.request.method == "POST":
        if not title:
            #we didn't get given a title
            errors.append("You didn't enter a title!")
        if len(title) > 50:
            errors.append("Your title was too long!")
        if not firstword:
            errors.append("You didn't enter a starting word!")
        if ' ' in firstword:
            errors.append("Please only enter one word")
        if len(firstword) > 25:
            errors.append("Your word is too long. Word must be below 26 characters long")
        author = get_current_user(response)
        if author is None:
            errors.append('You must be logged in to create a story')
        if not errors:
            #write to the database
            new_story = story.Story(title, firstword, author)
            story_id = new_story.story_id
            response.redirect("/story/" + str(story_id))
            return

        #if there are errors, relay back to user
        errors.append("Please try again.")

    variables = {
        'errors': errors,
        'user': get_current_user(response),
        'title': title,
        'firstword': firstword
    }

    response.write(render(
        "templates/createastory.html",
        variables,
    ))


def view_story(response, sid):
    story_inst = story.Story.from_id(sid)
    if not story_inst:
        raise tornado.web.HTTPError(404)

    render_stories(response, [story_inst])


def add_word(response, sid, wid):
    story_inst = story.Story.from_id(sid)
    word_inst = word.Word.from_id(wid)
    errors = []

    new_word = response.get_field("word").strip()

    if not new_word:
        errors.append("Please enter a word")

    if " " in new_word:
        errors.append("Please only enter one word")

    if len(new_word) > 50:
        errors.append("Your word is too long. Word must be below 51 characters long")

    author = get_current_user(response)
    if author is None:
        errors.append('You must be logged in to post a word')

    if not errors:  # if there are no errors
        word_inst.add_child(new_word, author)
        story_inst.prune()
        response.redirect("/story/{}".format(story_inst.story_id))
        return

    errors.append("Please try again.")

    variables = {
        'errors': errors,
        "story": story_inst,
        'user': get_current_user(response)
    }
    response.write(render(
        "templates/viewstory.html",
        variables,
    ))


def upvote(response, story_id, word_id):
    # TODO; actually use the errors

    author = get_current_user(response)
    errors = []
    if author is None:
        errors.append('You must be logged in to upvote a word')

    if response.request.method == "POST" and not errors:
        # Write to database
        word_inst = word.Word.from_id(word_id)
        word_inst.add_vote(author)

    response.redirect("/story/{}".format(story_id))


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
                    response.set_secure_cookie('username', username)
                    response.redirect('/')
                    return
                else:
                    login_fail = True
                    username = password = None
            else:
                username = password = None

        response.write(render(
            'templates/login.html',
            {'user': username, 'login_fail': login_fail}
        ))


def logout(response):
        response.clear_cookie('username')
        response.redirect('/')


def register(response):
        logged_name = response.get_secure_cookie('username')
        if logged_name is not None:
                response.redirect('/')
                return
        username = response.get_field('name')
        password = response.get_field('password')
        email = response.get_field('email')
        # the vars to pass to the register form
        p_username = username
        p_password = password
        p_email = email

        errors = []
        if username and password is not None:
            if EMAIL_RE.match(email) is None:
                errors.append('Invalid email')
            if re.match(r'^\w{3,12}$', username) is None:
                errors.append('Invalid username, usernames must be 3-12 characters and alphanumeric, optionally containing underscores')
            if user.User.from_username(username) is not None:
                errors.append('Invalid username, username already taken')
            if len(password) < 5:
                errors.append('Invalid password, passwords must be at least 5  characters long')
            if not errors:
                response.set_secure_cookie('username', username)
                user.User.create(username, password, email=email)
                response.redirect('/')
                return

            else:
                username = password = None
        else:
            username = password = None

        context = {
            'user': username,
            'errors': errors,
            'username': p_username,
            'password': p_password,
            'email': p_email
        }
        response.write(render(
            'templates/register.html',
            context
        ))


def profile(response, username):
        # get request, the list of stories they have made,
        # list of stories they have contributed to maybe, last visit?,
        display_user = user.User.from_username(username)
        current_user = get_current_user(response)

        context = {
            "current_user": current_user,
            "display_user": display_user
        }

        response.write(render(
            "templates/userProfile.html",
            context
        ))


def scoreboard(response):
    variables = {
        'users': user.User.user_list(),
        'user': get_current_user(response)
    }

    response.write(render(
        'templates/scoreboard.html',
        variables
    ))

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
    server.register('/mystories', my_stories)
    server.register('/scoreboard', scoreboard)
    server.register('/user/(\w+)', profile)
    server.run()
