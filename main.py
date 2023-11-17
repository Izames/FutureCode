from fastapi import FastAPI

import sqlite3

app = FastAPI()

def create_database():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (title text, author text, year integer)''')

    conn.commit()
    conn.close()




@app.on_event("startup")
def startup_event():
    create_database()


@app.get("/books")
def get_all_books():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()

    c.execute('SELECT * FROM books')
    rows = c.fetchall()

    conn.close()

    return {"books": rows}


@app.post("/books")
def add_book(title: str, author: str, year: int):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()

    c.execute('INSERT INTO books VALUES (?, ?, ?)', (title, author, year))

    conn.commit()
    conn.close()

    return {"message": "Book added successfully"}


@app.put("/books/{title}")
def update_book(title: str, new_title: str):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()

    c.execute('UPDATE books SET title = ? WHERE title = ?', (new_title, title))

    conn.commit()
    conn.close()

    return {"message": "Book updated successfully"}


@app.delete("/books/{title}")
def delete_book(title: str):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()

    c.execute('DELETE FROM books WHERE title = ?', (title,))

    conn.commit()
    conn.close()

    return {"message": "Book deleted successfully"}


@app.get("/books/search/{title}")
def search_book(title: str):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()

    c.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + title + '%',))
    rows = c.fetchall()

    conn.close()

    return {"books": rows}


def choose():
    ch = int(input("выберите действие: \n"
                   "1: просмотр всех книг\n"
                   "2: добавить книгу \n"
                   "3: изменить название книги \n"
                   "4: удалить книну\n"
                   "5: найти книгу\n"
                   "6: выйти"))
    match ch:
        case 1:
            get_all_books()
            choose()
        case 2:
            add_book()
            choose()
        case 3:
            update_book()
            choose()
        case 4:
            delete_book()
            choose()
        case 5:
            search_book()
            choose()

choose()