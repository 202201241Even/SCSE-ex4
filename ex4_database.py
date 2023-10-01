import ex4
import sqlite3


#In this program, you will initialize the database and add users.
def add_a_user(name, email):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (name, email) VALUES (?, ?)", (name, email))
    connection.commit()
    connection.close()

def get_user_information():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    user = cursor.fetchall()
    connection.close()
    return user

# ex4.db()
# add_a_user("James", "12344433@qq.com")

print(get_user_information())