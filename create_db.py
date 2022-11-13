import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Bhlohass*76'
    )

my_cursor = mydb.cursor()

# my_cursor.execute('CREATE DATABASE our_students')

my_cursor.execute('SHOW DATABASES')
for db in my_cursor:
    print(db)

'''
('codemy',)
('information_schema',)
('loginpage',)
('mysql',)
('our_students',)   <<====
('our_users',)
('performance_schema',)
('pos',)
('sakila',)
('second_db',)
('students',)
('sys',)
('world',)
'''