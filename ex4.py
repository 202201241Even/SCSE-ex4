import sqlite3
def db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT NOT NULL,
        status TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (book_id) REFERENCES Books (book_id),
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    )''')
    conn.commit()
    conn.close()

def main():
    def add_book(title, author, isbn):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        status = "Unordered"
        cursor.execute("INSERT INTO Books (title, author, isbn, status) VALUES (?, ?, ?, ?)",
                       (title, author, isbn, status))
        connection.commit()
        connection.close()

    def add_a_book():
        print("Please enter the information of the book:")
        book_title = input("Title:")
        book_author = input("Author:")
        book_isbn = input("ISBN：")
        add_book(book_title, book_author, book_isbn)

    def get_book_detail(book_id):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("SELECT status FROM Books WHERE book_id=?", (book_id,))
        status = cursor.fetchone()[0]
        if status == "Unordered":
            cursor.execute("SELECT * FROM Books WHERE book_id=?", (book_id,))
        else:
            cursor.execute("SELECT books.*, users.* FROM Books Inner Join Reservations ON Books.book_id = Reservations.book_id Inner Join Users ON Reservations.user_id = Users.user_id WHERE Books.book_id=?", (book_id,))
        books = cursor.fetchall()
        connection.close()
        return books


    def find_book_information():
        book_id = input("Please enter the book_ID:")
        result = get_book_detail(book_id)
        if result:
            print(result)
        else:
            print("Can't find the book, please try again.")

    def get_book_information(book_id):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Books WHERE book_id=?", (book_id,))
        book = cursor.fetchone()
        connection.close()
        return book

    def get_user_information(user_id):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Reservations WHERE user_id=?", (user_id,))
        user = cursor.fetchall()
        connection.close()
        return user

    def get_reservation_by_id(reservation_id):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Reservations WHERE reservation_id=?", (reservation_id,))
        reservationID = cursor.fetchall()
        connection.close()
        return reservationID

    def get_title_information(title):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Books WHERE title=?", (title,))
        id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM Reservations WHERE book_id=?", (id,))
        TITLE = cursor.fetchall()
        connection.close()
        return TITLE

    def find_reservation_by():
        input_string = input("Please enter the Book_ID(LB), User_ID(LU), Reservation_ID(LR) ,Title(choose one):")
        if input_string.startswith("LB"):
            result = get_book_information(input_string[2:])

        elif input_string.startswith("LU"):
            result = get_user_information(input_string[2:])

        elif input_string.startswith("LR"):
            result = get_reservation_by_id(input_string[2:])

        else:
            result = get_title_information(input_string)

        if result:
            print(result)
        else:
            print("Fail，please try again.")

    def get_all_books_detail():
        connection = sqlite3.connect("library.db")
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()
        cursor1.execute("SELECT * FROM Books where status='Unordered'")
        cursor2.execute("SELECT books.*, users.* FROM Books Inner Join Reservations ON Books.book_id = Reservations.book_id Inner Join Users ON Reservations.user_id = Users.user_id")
        books = cursor1.fetchall() + cursor2.fetchall()
        connection.close()
        return books

    def view_all_books():
        result = get_all_books_detail()
        if result:
            for item in result:
                print(item)
        else:
            print("There are no books.")

    def update_book_status(book_id, title, author, isbn, status, user_id):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        if status == "Unordered":
            cursor.execute("UPDATE Books SET title=?, author=?, isbn=?, status=? WHERE book_id=?", (title, author, isbn, status, book_id))
            cursor.execute("DELETE FROM Reservations WHERE book_id=?", (book_id,))

        else:
            cursor.execute("UPDATE Books SET title=?, author=?, isbn=?, status=? WHERE book_id=?", (title, author, isbn, status, book_id))
            cursor.execute("INSERT INTO Reservations (book_id, user_id, status) VALUES (?, ?, ?)", (book_id, user_id, status))
        connection.commit()
        connection.close()
        return cursor.rowcount > 0

    def update_book(book_id, title, author, isbn):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE Books SET title=?, author=?, isbn=? WHERE book_id=?", (title, author, isbn, book_id))
        connection.commit()
        connection.close()
        return cursor.rowcount > 0

    def update_book_information():
        book_id = input("Please input book_ID:")
        new_title = input("Please input title:")
        new_author = input("Please input  author name:")
        new_isbn = input("Please input ISBN:")
        new_status = input("Please input status（Note: There are only two states, Unordered or On reservation.）:")
        if new_status != None:
            new_user_id = input("Please enter user_ID:")
            success = update_book_status(book_id, new_title, new_author, new_isbn, new_status, new_user_id)
        else:
            success = update_book(book_id, new_title, new_author, new_isbn)
        if success:
            print("Successfully!")
        else:
            print("Can't find the book, please try again.")

    def delete(book_id):
        connection = sqlite3.connect("library.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Books  WHERE book_id=? ", (book_id,))
        connection.commit()
        connection.close()
        return cursor.rowcount > 0

    def delete_books():
        book_id = input("Please enter the book_ID you want to delete:")
        success = delete(book_id)
        if success:
            print("Successfully ")
        else:
            print("Can't find the book, please try again.")


    while True:
        print("\n****Library Management System****")
        print("1. Add a new book to the database")
        print("2. Find a book's details based on BookID")
        print("3. Find a book's reservation status based on BookID, Title, UserID, or ReservationID")
        print("4. Find all the books in the database")
        print("5. Modify/update book details based on BookID")
        print("6. Delete a book based on BookID")
        print("7. Exit")

        i = input("\nSelect the sequence number you want to perform the operation on: ")
        if i == "1":
            add_a_book()
        elif i == "2":
            find_book_information()
        elif i == "3":
            find_reservation_by()
        elif i == "4":
            view_all_books()
        elif i == "5":
            update_book_information()
        elif i == "6":
            delete_books()
        elif i == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()