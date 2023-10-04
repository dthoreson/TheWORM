from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DATABASE

from flask import flash

from flask_app.models import user

class Book:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.author = data["author"]
        self.num_of_pages = data["num_of_pages"]
        self.genre = data["genre"]
        self.description = data["description"]
        self.image = data["image"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        #OPTIONAL ATTRIBUTES
        # self.owner = None
        # self.status = data["status"]
        # self.my_notes = data["my_notes"]

        

#-------------- SHOW ALL BOOK FOR THE USER (READ ALL) --------------
    @classmethod
    def get_all_with_user(cls):
        # ALWAYS START THE JOIN WHERE THE FIRST TABLE MENTIONED WILL ALWAYS INCLUDE THE OTHER TABLE. IE A BOOK WILL ALWAYS BE ATTACHED TO A USER
        query = """
        SELECT * FROM books
        LEFT JOIN users ON
        books.user_id = users.id;"""
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        library = []
        for row in results:
            #CREATE THE BOOK
            book = cls(row)
            #CREATE THE USER DATA
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            #CREATE THE USER HERE AND SET EQUAL TO NEW BOOK OWNER ATTRIBUTE
            this_user = user.User(user_data)
            book.owner = this_user
            library.append(book)
        return library

#-------------- CREATE A BOOK (CREATE) --------------
    @classmethod
    def create(cls, data):
        query= """
        INSERT INTO books
        (title, author, num_of_pages, genre, description, image, user_id)
        VALUES
        (%(title)s, %(author)s, %(num_of_pages)s, %(genre)s, %(description)s, %(image)s, %(user_id)s);"""
        # ^^^ PREPARED STATEMENTS TO HELP PREVENT SQL INJECTION ^^^
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

#----------------- READ ONE BOOK (SHOW ONE) --------------------
    @classmethod
    def get_by_id(cls, id):
        #NEED TO DO DATA DICT IN ORDER TO PASS DATA TO THE QUERY METHOD BELOW
        data = {
            'id':id
        }
        query = """
        SELECT * FROM books
        JOIN users ON
        users.id = books.user_id
        WHERE books.id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            book = cls(results[0])
            row = results[0]
            user_data ={
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_user = user.User(user_data)
            book.owner = this_user
            return book
        return False

#----------------- EDIT BOOK METHOD -------------------
    @classmethod
    def update(cls, data):
    #THIS IS WHAT SAVES THE CHANGES OF THE BOOK INTO THE DB
        query = """UPDATE books
        SET title = %(title)s, author = %(author)s, image = %(image)s, genre = %(genre)s, num_of_pages = %(num_of_pages)s, description = %(description)s, updated_at = NOW() 
        WHERE id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query, data)

#------------------- GET ALL INFO FROM ONE BOOK ----------------
    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM books
        JOIN users ON books.user_id = users.id 
        WHERE books.id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])

#--------------- DELETE METHOD -----------------
    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM books 
        WHERE id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)

#---------------- BOOK VALIDATIONS ------------------
    @staticmethod
    def validate_book(book_data):
        is_valid = True
        if len(book_data["author"]) < 1:
            flash("Author name must be at least 1 character long.")
            is_valid= False
        if len(book_data['title']) < 1:
            flash("Book Title must be at least 1 character long.")
            is_valid= False
        if len(book_data['num_of_pages']) < 1:
            flash("The number of pages is required for book creation, an estimation works.")
            is_valid= False
        if len(book_data['genre']) < 1:
            flash("Book Genre must be at least 1 character long.")
            is_valid= False
        if len(book_data['description']) < 1:
            flash("Book Description must be at least 1 character long.")
            is_valid= False
        if len(book_data['image']) < 1:
            flash("Book Image URL link must be provided for book creation/edits.")
            is_valid= False
        return is_valid