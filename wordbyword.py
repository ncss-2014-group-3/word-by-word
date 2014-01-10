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
    title = str(response.get_field("title"))
    start_word = response.get_field("start_word")
    if title is None:
        #we didn't get given a title
    #TODO: We need to make sure the start word is actually a word, not numbers. Check the whitespace and also check the Title contains letters and that there is actually a title.
    check = re.match("^[A-Za-z0-9]([A-Za-z0-9!\"\(\)?',\.\:;]+|[A-Za-z0-9])*$", title)
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
server.register("/create", create)
server.register("/greet", greet)
server.run()
