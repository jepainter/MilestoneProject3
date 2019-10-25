"""
Imports of packages for functioning of site
"""
import os
from datetime import date
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, session, g)
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from forms import (RegistrationForm, UpdateProfileForm, LogInForm,
                   BookForm, CategoryForm, CommentForm, ReviewForm)

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


# Spacer to prevent collapse
"""
Landing page
"""
@app.route("/", methods=["GET"])
def home_screen():
    """
    Function for rendering landing page
    Check if user in session, type of user in order to render correct
    menus for nav
    """
    
    # Check to see type of user and render html and options
    if g.user:
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        if g.user == str(super_user["_id"]):
            return render_template(
                "index.html",
                categories=mongo.db.categories.find().sort("category_name"),
                super_user=g.user)
        else:
            return render_template(
                "index.html",
                categories=mongo.db.categories.find().sort("category_name"),
                regular_user=g.user)
    else:
        return render_template(
            "index.html",
            categories=mongo.db.categories.find().sort("category_name"))


# Spacer to prevent collapse
"""
Management (CRUD) of books collection in database
"""
@app.route("/get_books/", defaults={"category_id": ""},
           methods=["GET", "POST"])
@app.route("/get_books/<category_id>", methods=["GET", "POST"])
def get_books(category_id):
    """
    Function to fetch books from database and render to html.  Uses a
    new dictionary to display grouped information together
    """
    
    # Empty dict created to merge results from collections
    merged_result = {}
    
    # Retrieve books according to category, if not retrieve all books
    if category_id != "":
        books = mongo.db.books.find({"category_id": category_id}).sort("title")
    elif category_id == "":
        books = mongo.db.books.find().sort("title")

    # Populate new dictionary with results from book collection retrieval
    for book in books:
        for key, value in book.items():
            if key == "_id":
                merged_result[str(value)] = book

    # Update new dictionary with category information, if available
    for book_id, book_detail in merged_result.items():
        for key, value in book_detail.items():
            if key == "category_id":
                if value != "":
                    the_category = mongo.db.categories.find_one(
                        {"_id": ObjectId(value)})
                    if the_category is not None:
                        merged_result[book_id]["category_name"] = merged_result[book_id].pop(
                            "category_id")
                        for k, v in the_category.items():
                            if k == "category_name":
                                merged_result[book_id]["category_name"] = the_category[k]
                    else:
                        merged_result[book_id]["category_name"] = merged_result[book_id].pop(
                            "category_id")
                        merged_result[book_id]["category_name"] = "Not assigned yet"
                else:
                    merged_result[book_id]["category_name"] = merged_result[book_id].pop(
                        "category_id")
                    merged_result[book_id]["category_name"] = "Not assigned yet"
            else:
                pass
    
    # Check to see type of user and render html and options
    if g.user:
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        if g.user == str(super_user["_id"]):
            return render_template(
                "books.html",
                books=merged_result,
                categories=mongo.db.categories.find().sort("category_name"),
                super_user=g.user)
        else:
            return render_template(
                "books.html",
                books=merged_result,
                categories=mongo.db.categories.find().sort("category_name"),
                regular_user=g.user)
    else:
        return render_template(
            "books.html",
            books=merged_result,
            categories=mongo.db.categories.find().sort("category_name"))


@app.route("/get_book/<book_id>")
def get_book(book_id):
    """
    Function to get individual book details and render to html
    """
    
    # Retrieval of relevant info on book from collections
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    the_review = mongo.db.reviews.find_one({"book_id": book_id})
    the_comments = mongo.db.comments.find({"book_id": book_id})
    the_commenters = list(mongo.db.users.find())
    
    # Handling of missing info if any for book
    for book_k, book_v in the_book.items():
        if book_k == 'category_id' and book_v != "":
            the_category = mongo.db.categories.find_one(
                {"_id": ObjectId(book_v)})
            if the_category is None:
                the_category = {
                    "category_name": "Not assigned yet"
                }
        elif book_k == 'category_id' and book_v == "":
            the_category = {
                "category_name": "Not assigned yet"
            }
        elif book_k == 'user_id' and book_v != "":
            the_user = mongo.db.users.find_one({"_id": ObjectId(book_v)})
            if the_user is None:
                the_user = {
                    "username": "Anonymous"
                }
        elif book_k == 'user_id' and book_v == "":
            the_user = {
                "username": "Anonymous"
            }
    
    # Handling of missing info if any for review
    if the_review is not None:
        #for review_k, review_v in the_review.items():
            if the_review["user_id"] != "":
                the_reviewer = mongo.db.users.find_one(
                    {"_id": ObjectId(the_review["user_id"])})
                if the_reviewer is None:
                    the_reviewer = {
                        "username": "Anonymous"
                    }
            elif the_review['user_id'] == "":
                the_reviewer = {
                    "username": "Anonymous"
                }
            else:
                the_reviewer = {
                    "username": "Anonymous"
                }
                
    else:
        the_review = {
            "review": "Not reviewed yet",
            "date_added": "Not reviewed yet"
        }
        the_reviewer = {
            "username": "No reviewer yet"
        }
    
    # Check to see type of user and render html and options
    if g.user:
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        if g.user == str(super_user["_id"]):
            return render_template(
                "book.html",
                book=the_book,
                category=the_category,
                user=the_user,
                comments=the_comments,
                review=the_review,
                reviewer=the_reviewer,
                commenters=the_commenters,
                super_user=g.user)
        else:
            return render_template(
                "book.html",
                book=the_book,
                category=the_category,
                user=the_user,
                comments=the_comments,
                review=the_review,
                reviewer=the_reviewer,
                commenters=the_commenters,
                regular_user=g.user)
    else:
        return render_template(
            "book.html",
            book=the_book,
            category=the_category,
            user=the_user,
            comments=the_comments,
            review=the_review,
            reviewer=the_reviewer,
            commenters=the_commenters)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Function to load WTForm for adding book and render to html and add
    to database. Checks first whether a user is logged in, before
    performing function.
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    """
    
    # Check to see if user logged in and render html
    if g.user:
        form = BookForm()
        
        # Validation of form and insert in collection
        if form.validate_on_submit():
            flash(f"New book added: {form.title.data.title()}!", "success")
            book = {
                "title": form.title.data.lower(),
                "author_fname": form.author_fname.data.lower(),
                "author_lname": form.author_lname.data.lower(),
                "category_id": form.category_id.data,
                "user_id": g.user,
                "up_votes": 0,
                "down_votes": 0,
                "date_added": date.today().strftime("%Y/%m/%d"),
                "cover_url": form.cover_url.data,
                "csrf_token": form.csrf_token.data
            }
            books = mongo.db.books
            books.insert_one(book)
            return redirect(
                url_for(
                    "get_books",
                    _scheme="https",
                    _external=True))
        
        # Check to see type of user and return of form for correction
        else:
            super_user = mongo.db.users.find_one({"username": "ubradmin"})
            if g.user == str(super_user["_id"]):
                return render_template(
                    "addbook.html",
                    form=form,
                    categories=mongo.db.categories.find().sort("category_name"),
                    super_user=g.user)
            else:
                return render_template(
                    "addbook.html",
                    form=form,
                    categories=mongo.db.categories.find().sort("category_name"),
                    regular_user=g.user)
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/edit_book/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    """
    Function to load form for a book review and render to html. 
    Checks first whether a user is logged in, before performing
    function.
    """
    
    # Check to see if user logged in and render html
    if g.user:
        the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        
        # Check if user same as contributor or super user
        if g.user == the_book["user_id"] or g.user == str(super_user["_id"]):
            form = BookForm()
            all_categories = mongo.db.categories.find()
            
            # Validation of form and insert in collection
            if form.validate_on_submit():
                flash(
                    f"Book details successfully updated: {form.title.data.title()}!",
                    "success")
                books = mongo.db.books
                books.update({"_id": ObjectId(book_id)},
                             {
                    "title": form.title.data.lower(),
                    "author_fname": form.author_fname.data.lower(),
                    "author_lname": form.author_lname.data.lower(),
                    "category_id": form.category_id.data,
                    "user_id": g.user,
                    "up_votes": the_book["up_votes"],
                    "down_votes": the_book["down_votes"],
                    "date_added": date.today().strftime("%Y/%m/%d"),
                    "cover_url": form.cover_url.data,
                    "csrf_token": form.csrf_token.data
                })
                return redirect(
                    url_for(
                        "get_book",
                        book_id=book_id,
                        _scheme="https",
                        _external=True))
            
            # Check to see type of user and return of form for correction
            else:
                if g.user == str(super_user["_id"]):
                    return render_template(
                        "editbook.html",
                        book=the_book,
                        categories=all_categories,
                        form=form,
                        super_user=g.user)
                else:
                    return render_template(
                        "editbook.html",
                        book=the_book,
                        categories=all_categories,
                        form=form,
                        regular_user=g.user)
        else:
            flash(
                f"You cannot edit this book's details, as it was uploaded by someone else...",
                "danger")
            return redirect(
                url_for(
                    "get_book",
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    """
    Function to delete a book from the database, checks whether user
    is logged in and only allows user to delete own books submitted.
    Function deletes reviews and comments from db as well, as there
    is no use to keep info. Super user can delete any book and 
    associated reviews and comments.
    """
    
    # Check to see if user logged in and render html
    if g.user:
        the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        
        # Check if user same as contributor or super user, if yes delete
        if g.user == str(super_user["_id"]):
            flash(f"Book and associated info deleted by ADMIN!", "success")
            mongo.db.books.remove({"_id": ObjectId(book_id)})
            mongo.db.reviews.remove({"book_id": book_id})
            mongo.db.comments.remove({"book_id": book_id})
            return redirect(
                url_for(
                    'get_books',
                    _scheme="https",
                    _external=True))
        elif g.user == the_book["user_id"]:
            flash(f"Book and associated info deleted from site.", "success")
            mongo.db.books.remove({"_id": ObjectId(book_id)})
            mongo.db.reviews.remove({"book_id": book_id})
            mongo.db.comments.remove({"book_id": book_id})
            return redirect(
                url_for(
                    'get_books',
                    _scheme="https",
                    _external=True))
        else:
            flash(
                f"You cannot delete that book, as it was uploaded by someone else...",
                "danger")
            return redirect(
                url_for(
                    "get_books",
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


# Spacer to prevent collapse
"""
Management (CRUD) of categories collection in database
"""
@app.route("/get_categories")
def get_categories():
    """
    Function to fetch categories from database and render to html
    """
    
    all_categories = mongo.db.categories.find().sort("category_name")
    super_user = mongo.db.users.find_one({"username": "ubradmin"})
    
    # Check user type for options regarding collection
    if g.user == str(super_user["_id"]):
        return render_template(
            "categories.html",
            categories=all_categories,
            super_user=g.user)
    elif g.user:
        return render_template(
            "categories.html",
            categories=all_categories,
            regular_user=g.user)
    else:
        return render_template("categories.html", categories=all_categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    Function to load WTForm for adding category and render to html and
    add to database.  Checks first whether a user is logged in, before
    performing function.
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    """
    
    super_user = mongo.db.users.find_one({"username": "ubradmin"})
    
    # Check if super user to add category
    if g.user == str(super_user["_id"]):
        form = CategoryForm()
        if form.validate_on_submit():
            flash(
                f"New category created: {form.category_name.data}!",
                "success")
            category = {
                "category_name": form.category_name.data.lower(),
                "cover_url": form.cover_url.data,
                "csrf_token": form.csrf_token.data
            }
            categories = mongo.db.categories
            categories.insert_one(category)
            return redirect(
                url_for(
                    "get_categories",
                    _scheme="https",
                    _external=True))
        else:
            return render_template(
                "addcategory.html",
                form=form,
                super_user=g.user)
    else:
        flash(
            f"You cannot add categories, you do not have the correct privileges...",
            "danger")
        return redirect(
            url_for(
                "get_categories",
                _scheme="https",
                _external=True))


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """
    Function to load form for a category to be changed and render to
    html. Checks first whether a user is logged in, before performing
    function.
    """

    super_user = mongo.db.users.find_one({"username": "ubradmin"})
    
    # Check if super user to edit category
    if g.user == str(super_user["_id"]):
        form = CategoryForm()
        the_category = mongo.db.categories.find_one(
            {"_id": ObjectId(category_id)})
        if form.validate_on_submit():
            flash(
                f"Category successfully edited: {form.category_name.data}!",
                "success")
            categories = mongo.db.categories
            categories.update({"_id": ObjectId(category_id)},
                              {
                "category_name": form.category_name.data.lower(),
                "cover_url": form.cover_url.data,
                "csrf_token": form.csrf_token.data
            })
            return redirect(
                url_for(
                    "get_categories",
                    _scheme="https",
                    _external=True))
        else:
            return render_template(
                "editcategory.html",
                category=the_category,
                form=form,
                super_user=g.user)
    else:
        flash(
            f"You cannot edit categories, you do not have the correct privileges...",
            "danger")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """
    Function to delete a category from the database, check first if
    user logged in
    """
    
    super_user = mongo.db.users.find_one({"username": "ubradmin"})
    
    # Check if super user to delete category
    if g.user == str(super_user["_id"]):
        flash(f"Category successfully deleted!", "success")
        mongo.db.categories.remove({"_id": ObjectId(category_id)})
        return redirect(
            url_for(
                "get_categories",
                _scheme="https",
                _external=True))
    else:
        flash(
            f"You cannot delete categories, you do not have the correct privileges...",
            "danger")
        return redirect(
            url_for(
                "get_categories",
                _scheme="https",
                _external=True))


# Spacer to prevent collapse
"""
Management (CRUD) of up and down votes in database
"""
@app.route("/up_vote/<book_id>", methods=["GET", "POST"])
def up_vote(book_id):
    """
    Function to add an up vote to a book.  Up votes are not dependent
    on user being logged in, visitors can vote.
    """
    
    books = mongo.db.books
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    new_up_vote = the_book["up_votes"] + 1
    books.update_one({"_id": ObjectId(book_id)}, {
                     "$set": {"up_votes": new_up_vote}})
    return redirect(
        url_for(
            "get_book",
            book_id=book_id,
            _scheme="https",
            _external=True))


@app.route("/down_vote/<book_id>", methods=["GET", "POST"])
def down_vote(book_id):
    """
    Function to down an up vote to a book.  Up votes are not dependent
    on user being logged in, visitors can vote
    """
    
    books = mongo.db.books
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    new_down_vote = the_book["down_votes"] + 1
    books.update_one({"_id": ObjectId(book_id)},
                     {"$set": {"down_votes": new_down_vote}})
    return redirect(
        url_for(
            "get_book",
            book_id=book_id,
            _scheme="https",
            _external=True))


# Spacer to prevent collapse
"""
Management (CRUD) of reviews collection in database
"""
@app.route("/check_review_exists/<book_id>")
def check_review_exists(book_id):
    """
    Function to check if a review exists already, if so, then pass back
    to the get_book page.  If not, proceed to add_review function
    """

    a_review = mongo.db.reviews.find_one({"book_id": book_id})
    if a_review is not None:
        flash(f"A review already exists for the book", "warning")
        return redirect(
            url_for(
                'get_book',
                book_id=book_id,
                _scheme="https",
                _external=True))
    else:
        
        # Check if user logged in before adding a review
        if g.user:
            return redirect(
                url_for(
                    "add_review",
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
        else:
            flash(f"You need to log in first...", "warning")
            return redirect(
                url_for(
                    "log_user_in",
                    _scheme="https",
                    _external=True))


@app.route("/add_review/<book_id>", methods=["GET", "POST"])
def add_review(book_id):
    """
    Function to load WTForm for adding review on book
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    """
    
    # Check if user logged in
    if g.user:
        form = ReviewForm()
        
        # Validation of form and insert in collection
        if form.validate_on_submit():
            flash(f"New review uploaded!", "success")
            review = {
                "review": form.review.data,
                "book_id": book_id,
                "user_id": g.user,
                "date_added": date.today().strftime("%Y/%m/%d"),
                "csrf_token": form.csrf_token.data
            }
            reviews = mongo.db.reviews
            reviews.insert_one(review)
            return redirect(
                url_for(
                    "get_book",
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
        
        # Check to see type of user and return of form for correction
        else:
            super_user = mongo.db.users.find_one({"username": "ubradmin"})
            if g.user == str(super_user["_id"]):
                return render_template(
                    "addreview.html",
                    form=form,
                    book_id=book_id,
                    super_user=g.user)
            else:
                return render_template(
                    "addreview.html",
                    form=form,
                    book_id=book_id,
                    regular_user=g.user)
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/edit_review/<book_id>", methods=["GET", "POST"])
def edit_review(book_id):
    """
    Function to load form for a review to be changed and render to
    html. Checks first whether a user is logged in and whether user
    is same as original reviewer before performing function.
    """
    
    # Check if user logged in
    if g.user:
        the_review = mongo.db.reviews.find_one({"book_id": book_id})
        
        # Check if user same as reviewer
        if g.user == the_review["user_id"]:
            form = ReviewForm()
            if form.validate_on_submit():
                flash(f"Review successfully edited!", "success")
                reviews = mongo.db.reviews
                reviews.update({"_id": ObjectId(the_review["_id"])},
                               {
                    "review": form.review.data,
                    "book_id": book_id,
                    "user_id": g.user,
                    "date_added": date.today().strftime("%Y/%m/%d"),
                    "csrf_token": form.csrf_token.data
                })
                return redirect(
                    url_for(
                        "get_book",
                        book_id=book_id,
                        _scheme="https",
                        _external=True))
            
            # Check user type and render relevant options
            else:
                super_user = mongo.db.users.find_one({"username": "ubradmin"})
                if g.user == str(super_user["_id"]):
                    return render_template(
                        "editreview.html",
                        book_id=book_id,
                        review=the_review,
                        form=form,
                        super_user=g.user)
                else:
                    return render_template(
                        "editreview.html",
                        book_id=book_id,
                        review=the_review,
                        form=form,
                        regular_user=g.user)
        else:
            flash(
                f"You cannot edit this review, as it was uploaded by someone else...",
                "danger")
            return redirect(
                url_for(
                    "get_book",
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/delete_review/<book_id>")
def delete_review(book_id):
    """
    Function to delete a review from the database, checks whether user
    is logged in and only allows user to delete own reviews. Super
    user can delete any reviews.
    """
    
    # Check if user logged in
    if g.user:
        the_review = mongo.db.reviews.find_one({"book_id": book_id})
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        
        # Check user type for relevant options
        if g.user == str(super_user["_id"]):
            flash(f"User review deleted by ADMIN!", "success")
            mongo.db.reviews.remove({"_id": the_review["_id"]})
            return redirect(
                url_for(
                    'get_book',
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
        elif g.user == the_review["user_id"]:
            flash(f"Review deleted from site.", "success")
            mongo.db.reviews.remove({"_id": the_review["_id"]})
            return redirect(
                url_for(
                    'get_book',
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
        else:
            flash(
                f"You cannot delete the review, as it was uploaded by someone else...",
                "danger")
            return redirect(
                url_for(
                    'get_book',
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


# Spacer to prevent collapse
"""
Management (CRUD) of comments collection in database
"""
@app.route("/add_comment/<book_id>", methods=["GET", "POST"])
def add_comment(book_id):
    """
    Function to load WTForm for adding comment on book
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    """
    
    # Check if user logged in
    if g.user:
        form = CommentForm()
        
        # Check form and validate before insert
        if form.validate_on_submit():
            flash(f"New comment posted!", "success")
            comment = {
                "comment": form.comment.data,
                "book_id": book_id,
                "user_id": g.user,
                "csrf_token": form.csrf_token.data
            }
            comments = mongo.db.comments
            comments.insert_one(comment)
            return redirect(
                url_for(
                    "get_book",
                    book_id=book_id,
                    _scheme="https",
                    _external=True))
        
        # Checks user type to return form for comments
        else:
            super_user = mongo.db.users.find_one({"username": "ubradmin"})
            if g.user == str(super_user["_id"]):
                return render_template(
                    "addcomment.html",
                    form=form,
                    book_id=book_id,
                    super_user=g.user)
            else:
                return render_template(
                    "addcomment.html",
                    form=form,
                    book_id=book_id,
                    regular_user=g.user)
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/edit_comment/<comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    """
    Function to load WTForm for edit a comment on book
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    """
    
    # Check if user logged in
    if g.user:
        the_comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
        
        # Check if user same contributor or super user
        if g.user == the_comment["user_id"]:
            form = CommentForm()
            if form.validate_on_submit():
                flash(f"Comment successfully edited!", "success")
                comments = mongo.db.comments
                comments.update({"_id": ObjectId(comment_id)},
                                {
                    "comment": form.comment.data,
                    "book_id": the_comment["book_id"],
                    "user_id": g.user,
                    "csrf_token": form.csrf_token.data
                })
                return redirect(
                    url_for(
                        "get_book",
                        book_id=the_comment["book_id"],
                        _scheme="https",
                        _external=True))
            else:
                super_user = mongo.db.users.find_one({"username": "ubradmin"})
                if g.user == str(super_user["_id"]):
                    return render_template(
                        "editcomment.html",
                        form=form,
                        comment=the_comment,
                        super_user=g.user)
                else:
                    return render_template(
                        "editcomment.html",
                        form=form,
                        comment=the_comment,
                        regular_user=g.user)
        else:
            flash(
                f"You cannot edit this comment, as it was made by someone else...",
                "danger")
            return redirect(
                url_for(
                    'get_book',
                    book_id=the_comment["book_id"],
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    """
    Function to delete a review from the database, checks whether user
    is logged in and only allows user to delete own reviews.  Super
    user can delete any comments.
    """
    
    # Check if same user or super user for deletion
    if g.user:
        the_comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        if g.user == str(super_user["_id"]):
            flash(f"User comment deleted by ADMIN!", "success")
            mongo.db.comments.remove({"_id": the_comment["_id"]})
            return redirect(
                url_for(
                    'get_book',
                    book_id=the_comment["book_id"],
                    _scheme="https",
                    _external=True))
        elif g.user == the_comment["user_id"]:
            flash(f"Comment deleted from for book.", "success")
            mongo.db.comments.remove({"_id": the_comment["_id"]})
            return redirect(
                url_for(
                    'get_book',
                    book_id=the_comment["book_id"],
                    _scheme="https",
                    _external=True))
        else:
            flash(
                f"You cannot delete the comment, as it was made by someone else...",
                "danger")
            return redirect(
                url_for(
                    'get_book',
                    book_id=the_comment["book_id"],
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


# Spacer to prevent collapse
"""
Management (CRUD) of users collection in database
"""
@app.route("/get_users")
def get_users():
    """
    Function to fetch users from database and render to html
    """
    
    # Check if user logged in
    if g.user:
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        
        # Check user type for relevant info rendering
        if g.user == str(super_user["_id"]):
            users = mongo.db.users.find()
            return render_template(
                "users.html", users=users, super_user=g.user)
        else:
            user = mongo.db.users.find_one({"_id": ObjectId(g.user)})
            return render_template(
                "users.html", user=user, regular_user=g.user)
    else:
        flash(f"You need to login first...", "warning")
        return redirect(
            url_for(
                'log_user_in',
                _scheme="https",
                _external=True))


def user_exists(search_type, user_detail):
    """
    Function to validate if username or email is already taken in
    database, provides assistance to add_user function
    """

    the_user = mongo.db.users.find_one({str(search_type): str(user_detail)})
    if the_user is not None:
        return True
    else:
        return False


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """
    Function to load WTForm for user registration and render to html,
    and write to database. WTForms code adapted from Corey Shafer's
    tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    User authentication code adapted from from Corey Shafer's tutorial
    found at
    https://www.youtube.com/watch?v=CSHx6eCkmv0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=6
    """
    
    # Checks that a user is not logged in
    if g.user is None:
        form = RegistrationForm()
        if form.validate_on_submit():
            
            # Checks that info not same as other user in collection
            username_exist = user_exists(
                "username", form.username.data.lower())
            email_exist = user_exists("email", form.email.data.lower())
            username_error = "That username already exists.  Please choose a different one..."
            email_error = "That email already exists.  Please choose a different one..."
            
            # Redirect back to form if info already exists
            if username_exist and email_exist:
                return render_template(
                    "adduser.html",
                    form=form,
                    username_error=username_error,
                    email_error=email_error)
            elif username_exist and email_exist != True:
                return render_template(
                    "adduser.html", form=form, username_error=username_error)
            elif username_exist != True and email_exist == True:
                return render_template(
                    "adduser.html", form=form, email_error=email_error)
            
            # Encryption of password prior to storage in database
            hash_password = bcrypt.generate_password_hash(
                form.password.data).decode("utf-8")
            flash(
                f"Account created for {form.username.data}! You are free to log in...",
                "success")
            user = {
                "fname": form.fname.data.lower(),
                "lname": form.lname.data.lower(),
                "email": form.email.data.lower(),
                "username": form.username.data.lower(),
                "password": hash_password,
                "csrf_token": form.csrf_token.data
            }
            users = mongo.db.users
            users.insert_one(user)
            return redirect(
                url_for(
                    "log_user_in",
                    _scheme="https",
                    _external=True))
        else:
            return render_template("adduser.html", form=form)
    else:
        flash(f"You are already logged on!", "warning")
        return redirect(
            url_for(
                'home_screen',
                _scheme="https",
                _external=True))


@app.route("/log_user_in", methods=["GET", "POST"])
def log_user_in():
    """
    Function to load WTForm for user log in and render to html
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    Login functionality adapted from Pretty Printed's tutorial found at
    https://www.youtube.com/watch?v=eBwhBrNbrNI
    """
    
    form = LogInForm()
    session.pop("user", None)
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"email": form.email.data.lower()})
        if user is not None:
            for k, v in user.items():
                if k == "password":
                    if user and bcrypt.check_password_hash(
                            v, form.password.data):
                        flash(
                            f"Log in successful!",
                            "success")
                        session["user"] = str(user["_id"])
                        return redirect(
                            url_for(
                                'home_screen',
                                _scheme="https",
                                _external=True))
                    else:
                        flash(
                            f"Log in unsuccessful!  Check your email and password.",
                            "warning")
        else:
            flash(
                f"Log in unsuccessful!  Check your email and password.",
                "warning")
    return render_template("loginuser.html", form=form)


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    """
    Function to load form for a user to be editted and render to html
    """
    
    # Check if user logged in to edit details
    if g.user:
        the_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if g.user == str(the_user["_id"]):
            form = UpdateProfileForm()
            if form.validate_on_submit():
                username_exist = user_exists(
                    "username", form.username.data.lower())
                email_exist = user_exists("email", form.email.data.lower())
                username_error = "That username already exists.  Please choose a different one..."
                email_error = "That email already exists.  Please choose a different one..."
                if username_exist and email_exist:
                    if the_user["username"] != form.username.data.lower(
                    ) and the_user["email"] != form.email.data.lower():
                        return render_template(
                            "edituser.html",
                            form=form,
                            username_error=username_error,
                            email_error=email_error,
                            user=the_user,
                            regular_user=g.user)
                    elif the_user["username"] == form.username.data.lower() and the_user["email"] != form.email.data.lower():
                        return render_template(
                            "edituser.html",
                            form=form,
                            email_error=email_error,
                            user=the_user,
                            regular_user=g.user)
                    elif the_user["username"] != form.username.data.lower() and the_user["email"] == form.email.data.lower():
                        return render_template(
                            "edituser.html",
                            form=form,
                            username_error=username_error,
                            user=the_user,
                            regular_user=g.user)
                elif username_exist and email_exist != True:
                    if the_user["username"] != form.username.data.lower():
                        return render_template(
                            "edituser.html",
                            form=form,
                            username_error=username_error,
                            user=the_user,
                            regular_user=g.user)
                elif username_exist != True and email_exist == True:
                    if the_user["email"] != form.email.data.lower():
                        return render_template(
                            "edituser.html",
                            form=form,
                            email_error=email_error,
                            user=the_user,
                            regular_user=g.user)
                flash(
                    f"Account profile updated! You need to log in again...",
                    "success")
                users = mongo.db.users
                users.update({"_id": ObjectId(user_id)},
                             {
                    "fname": form.fname.data.lower(),
                    "lname": form.lname.data.lower(),
                    "email": form.email.data.lower(),
                    "username": form.username.data.lower(),
                    "password": the_user["password"],
                    "csrf_token": form.csrf_token.data
                })
                return redirect(
                    url_for(
                        'close_session',
                        _scheme="https",
                        _external=True))
            else:
                return render_template(
                    "edituser.html",
                    form=form,
                    user=the_user,
                    regular_user=g.user)
        else:
            flash(
                f"You cannot edit this user profile, as it belongs to someone else...",
                "danger")
            return redirect(
                url_for(
                    'get_users',
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    """
    Function to delete a user from the database, checks whether user
    is logged in and only allows user to delete own account.  Deleting
    user account will also delete the users comments, but not the 
    review.  Super user can delete any account and associated comments.
    """
    
    # Check user logged in status and determine type
    if g.user:
        super_user = mongo.db.users.find_one({"username": "ubradmin"})
        if g.user == str(super_user["_id"]):
            flash(
                f"User profile and associated comments deleted by ADMIN!",
                "success")
            mongo.db.users.remove({"_id": ObjectId(user_id)})
            mongo.db.comments.remove({"user_id": user_id})
            return redirect(
                url_for(
                    "get_users",
                    _scheme="https",
                    _external=True))
        elif g.user == user_id:
            flash(f"User profile and associated comments deleted", "success")
            mongo.db.users.remove({"_id": ObjectId(user_id)})
            mongo.db.comments.remove({"user_id": user_id})
            return close_session()
        else:
            flash(
                f"You cannot remove this user, you do not have the relevant privileges...",
                "danger")
            return redirect(
                url_for(
                    "get_users",
                    _scheme="https",
                    _external=True))
    else:
        flash(f"You need to log in first...", "warning")
        return redirect(
            url_for(
                "log_user_in",
                _scheme="https",
                _external=True))


# Spacer to prevent collapse
"""
Functions to assist with session management
"""
@app.route("/get_session")
def get_session():
    """
    Function to check session status
    """
    
    if "user" in session:
        return redirect(
            url_for(
                'home_screen',
                _scheme="https",
                _external=True))
    else:
        return redirect(
            url_for(
                'log_user_in',
                _scheme="https",
                _external=True))


@app.route("/close_session")
def close_session():
    """
    Function to force closure of session
    Session closure adapted from Pretty Printed's tutorial found at
    https://www.youtube.com/watch?v=eBwhBrNbrNI
    """
    session.pop("user", None)
    return redirect(
        url_for(
            'log_user_in',
            _scheme="https",
            _external=True))


@app.before_request
def before_request():
    """
    Login status adapted from Pretty Printed's tutorial found at
    https://www.youtube.com/watch?v=eBwhBrNbrNI
    """
    
    # Set session for user
    g.user = None
    if "user" in session:
        g.user = session["user"]


# Spacer to prevent collapse
"""
Call to run the app
"""
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
