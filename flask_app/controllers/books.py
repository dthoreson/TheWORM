from flask import render_template, request, redirect, session, flash, jsonify

from flask_app import app

from flask_app.models.user import User
from flask_app.models.book import Book

#---------- SHOW MY LIBRARY RENDER PAGE -------------
@app.route('/my_library')
def my_library():
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/main')
    data = {
        'id': session['uid']
    }
    #THIS WILL GIVE US ALL THE BOOKS
    library=Book.get_all_with_user()
    return render_template("my_library.html", logged_in_user=User.get_by_id(data), library=library)

#----------- SHOW ONE BOOK RENDER PAGE ON MYLIBRARY PAGE ---------------
@app.route('/show_one/<int:id>')
def my_book(id):
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
    my_book = Book.get_by_id(id)
    my_image = my_book.image.decode('utf-8')
    print(my_image)
    return render_template("show_my_book.html", my_book=my_book, my_image=my_image)

#----------- RESULTS API PROCESS ROUTE TO REDIRECT TO RESULTS RENDER HTML ROUTE (POST-REDIRECT) -----------
@app.route('/results', methods=["POST"])
def results():
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
    return redirect('/dashboard')

#------------ SAVE BOOK FROM API SEARCH BUTTON -------------------
@app.route('/save_book', methods=['POST'])
def save_book():
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
    bookInfo = {
        **request.form,
        'user_id': session['uid']
    }
    Book.create(bookInfo)
    return redirect('/dashboard')

#--------------CREATE BOOK FROM FORM OPTION ----------------------
@app.route('/create_book', methods=['POST'])
def create_book():
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
    if not Book.validate_book(request.form):
        return redirect('/create_book_form')
    Book.create(request.form)
    return redirect('/dashboard')

#------------ SHOW ALL RESULTS RENDER PAGE ----------------
@app.route('/show_results')
def show_results():
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
    data = {
        'id': session['uid']
    }
    user_id=User.get_by_id(data)
    print(user_id)
    return render_template("results.html", user_id=user_id)

#------------ CREATE BOOK FORM RENDER PAGE --------------------
@app.route('/create_book_form')
def book_form():
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
    data = {
        'id': session['uid']
    }
    user_id=User.get_by_id(data)
    print(user_id)
    return render_template("create_book.html", user_id=User.get_by_id(data))

#------------ THIS IS THE RENDER EDIT PAGE ----------------- 
@app.route('/edit/book/<int:id>')
def edit_book(id):
    if "uid" not in session:
        return redirect('logout')
    book=Book.get_by_id(id)
    book_image = book.image.decode('utf-8')
    print(book_image)
    return render_template("edit_book.html", book=book, book_image=book_image)

#------------------- THIS IS THE POST METHOD ACTION FOR EDITING A BOOK  -------------------------------------
@app.route('/update/book', methods=["POST"])
def update_book():
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
#THIS IS TO ENSURE WE MOVE FORWARD WITH EDIT PROCESS ONLY IF THE INFO IS VALIDATED. IF NOT RETURNS TO THE EDIT FORM.
    if not Book.validate_book(request.form):
        #THIS IS THE BOOK ID NEEDED IN ORDER TO REROUTE US BACK TO THE RENDER EDIT ROUTE
        return redirect(f'/edit/book/{request.form["id"]}')
    data ={
        "title": request.form["title"],
        "image": request.form["image"],
        "num_of_pages": request.form["num_of_pages"],
        "author": request.form["author"],
        "genre": request.form["genre"],
        "description": request.form["description"],
        #THIS IS THE BOOK ID
        "id": request.form["id"]
    }
#THIS IS WHERE ONCE WE PASS THE TWO CHECKS ABOVE, WE ACTUALLY CALL THE UPDATE(DATA) FUNCTION TO THE BOOK CLASS.
    Book.update(data)
    return redirect('/dashboard')

#------------- DELETE ----------------
@app.route('/book/<int:id>/delete')
def delete(id):
    if not 'uid' in session:
        flash("Access Denied, please Login!")
        return redirect('/logout')
    data = {
        'id': id
    }
    Book.delete(data)
    return redirect('/my_library')