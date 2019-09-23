"""
Imports of packages for functioning of site
"""
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

MONGODB_URI = os.getenv("MONGO_URI")

#app.config["MONGO_DBNAME"]
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route("/")
def home_screen():
    """
    Function for rendering landing page
    """
    return render_template("index.html")

@app.route("/get_books")
def get_books():
    """
    Function to fetch books from database and render to html
    """
    return render_template("books.html", books=mongo.db.books.find())

@app.route("/add_book")
def add_book():
    """
    Function to load form for a book review and render to html
    """
    return render_template("addbook.html", categories=mongo.db.categories.find())

@app.route("/insert_book", methods=["POST"])
def insert_book_review():
    """
    Function to insert a book review into the database
    """
    books = mongo.db.books
    books.insert_one(request.form.to_dict())
    """
    TO DO: add validation of input/required fields
    """
    return redirect(url_for("get_books"))

@app.route("/edit_book/<book_id>")
def edit_book(book_id):
    """
    Function to load form for a book review and render to html
    """
    
    """
    TO DO: add functionality to only edit book review if same poster
    """
    
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    all_categories = mongo.db.categories.find()
    return render_template("editbook.html", book=the_book, categories=all_categories)

@app.route("/update_book/<book_id>", methods=["POST"])
def update_book(book_id):
    """
    Function to update database with revised information
    """
    
    """
    TO DO: add additional items for complete record
    """
    
    books = mongo.db.books
    books.update({"_id": ObjectId(book_id)},
    {
        "title" : request.form.get("title"),
        "author_fname" : request.form.get("author_fname"),
        "author_lname" : request.form.get("author_lname"),
        "categoryid" : request.form.get("categoryid"),
        "review" : request.form.get("review")
    })
    return redirect(url_for("get_books"))

@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    """
    Function to delete a book from the database
    """
    mongo.db.books.remove({"_id" : ObjectId(book_id)})
    return redirect(url_for("get_books"))

@app.route("/get_categories")
def get_categories():
    """
    Function to fetch categories from database and render to html
    """
    return render_template("categories.html", categories=mongo.db.categories.find())

@app.route("/add_category")
def add_category():
    """
    Function to load form for adding category and render to html
    """
    return render_template("addcategory.html")

@app.route("/insert_category", methods=["POST"])
def insert_category():
    """
    Function to insert a category into the database
    """
    categories = mongo.db.categories
    categories.insert_one(request.form.to_dict())
    return redirect(url_for("get_categories"))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

