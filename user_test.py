from database.story import Story
from database.user import User
u = User.create(input('Username: '),input('Password: '))
s = Story(input('Title: '),input('First word: '),u)
