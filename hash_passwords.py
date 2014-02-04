from database import connection
from database import user

cursor = connection.cursor()
cursor.execute('''ALTER TABLE users ADD COLUMN salt TEXT NULL''')
results = cursor.execute('SELECT username,password,salt FROM users').fetchall()
for u in results:
    if u[2] is None:
        uo = user.User.from_username(u[0])
        print(
            '{}\'s password is not hashed (detected NULL salt). '
            'Performing hash on password...'.format(uo.username)
        )
        uo.update(u[1])
        print('Successfully hashed ' + uo.username + '\'s password.')
