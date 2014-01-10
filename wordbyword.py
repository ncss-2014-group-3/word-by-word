from tornado.ncss import Server
import db 
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
    start_word = response.get_field("start_word")
    #write them to the database
    db.create_story(title, start_word)

    #TODO: We need to make sure the start word is actually a word, not numbers. 
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
