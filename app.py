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

@app.route("/insert_book_review", methods=["POST"])
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
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

