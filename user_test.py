from database.user import User
u = User.create('Domo', 'blah') # user already exists, so return false
print('False:', u) # False - user exists

print()
u = User.from_username('Domo') # Returns user object
print('Object:', u) # User object
print('Username:', u.username) # Domo

print()
print('False:', u.login('Domo', 'aweifohweof')) # False
print('False:', u.login('Domo', 'hah')) # False

print()
u.update('Domo', 'hah', 'blah') # Update password in database - new = 'blah'
print('False:', u.login('Domo', 'hah')) # return false - user has been updated!
print('Object:', u.login('Domo', 'blah')) # return User object

print()
n = User.create('Nathan', 'hardy') # User already exists
print('False:', n)
