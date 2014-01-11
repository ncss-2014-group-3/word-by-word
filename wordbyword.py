from tornado.ncss import Server
#import db
import re
def index(response):
    response.write("Welcome to Spyware Exchange!")
    i = 0
    while i != 100:
        response.write(str(i) + "\n")
        i += 1

def hello(response, name):
    response.write("Hello " + name + " ")

def create(response):
    invalid_word = False
    #get the variables we need using get_field
    title = response.get_field("title")
    start_word = response.get_field("firstword")
    # a list of strings of things that went wrong
    #we will give this to the template.
    errors = []
    if response.request.method == "POST":
        if title is None:
            #we didn't get given a title
            errors.append("You didn't enter a title!")
        if len(title) > 50:
            errors.append("Your title was too long!")
        if start_word is None:
            errors.append("You didn't enter a starting word!")  
        if ' ' in start_word:
            errors.append("Please only enter one word.")
        if errors:
            errors.append("Please try again.")
        
       
            
        
    #word_che
    if " " in title:
        if check == True:
            print("yeyeyeye")        
    elif " " not in title:        
        if check == True:
            print("yeyeyeye")
        else:
            print("OH GOD SWEET JESUS NO!")
    title = title[0].upper() + title[1:]
    print(title)
    print(start_word)
    #write them to the database
    #db.create_story(title, start_word)

    
    response.write("""
    <html>
    <head>
    <title> Create A Story </title>
    </head>


    <body>
    <strong>This is the create page</strong>
    </body>

    </html>
    """)


    

def greet(response):
    fname = response.get_field('fname', 'James')
    lname = response.get_field('lname', 'Curran')
    response.write("Hello " + fname + " " + lname + "!")

    
server = Server()
server.register("/", index)
server.register("/hello/([a-z]+)", hello)
server.register("/story", create)
server.register("/greet", greet)
server.run()
