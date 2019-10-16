"""
Imports of packages for functioning of site
"""
import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from forms import RegistrationForm, LogInForm, AddBookForm, CategoryForm, AddCommentForm, AddReviewForm

app = Flask(__name__)

MONGODB_URI = os.getenv("MONGO_URI")

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route("/", methods=["GET"])
#@app.route("/home_screen", methods=["GET"]) #remove this if not necessary, test first
def home_screen():
    """
    Function for rendering landing page
    """
    return render_template("index.html", categories=mongo.db.categories.find())


"""
Management (CRUD) of books collection in database
"""
@app.route("/get_books/", defaults={"category_id": ""}, methods=["GET","POST"])
@app.route("/get_books/<category_id>", methods=["GET","POST"])
def get_books(category_id):
    """
    Function to fetch books from database and render to html
    """
    
    merged_result={}
    
    if category_id != "":
        books=mongo.db.books.find({"category_id": category_id})
   
    elif category_id == "":
        books=mongo.db.books.find()
    
    #Populate new dictionary with results from book collection retrieval
    for book in books:
        for key, value in book.items():
            if key == "_id":
                merged_result[str(value)] = book
    
    #Update new dictionary with category information
    for book_id, book_detail in merged_result.items():
        for key, value in book_detail.items():
            if key == "category_id":
                if value != "":
                    the_category=mongo.db.categories.find_one({"_id": ObjectId(value)})
                    if the_category != None:
                        merged_result[book_id]["category_name"] = merged_result[book_id].pop("category_id")
                        for k, v in the_category.items():
                            if k == "category_name":
                                merged_result[book_id]["category_name"] = the_category[k]
                    else:
                        merged_result[book_id]["category_name"] = merged_result[book_id].pop("category_id")
                        merged_result[book_id]["category_name"] = "Not assigned yet"
                else:
                    merged_result[book_id]["category_name"] = merged_result[book_id].pop("category_id")
                    merged_result[book_id]["category_name"] = "Not assigned yet"
            else:
                pass
    
    return render_template("books.html", books=merged_result, categories=mongo.db.categories.find())


@app.route("/get_book/<book_id>")
def get_book(book_id):
    """
    Function to get individual book details and render to html
    """
    
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    the_review = mongo.db.reviews.find_one({"book_id" : book_id})
    the_comments = mongo.db.comments.find({"book_id" : book_id})
    the_commenters = list(mongo.db.users.find())

    for book_k, book_v in the_book.items():
        if book_k == 'category_id' and book_v != "":    
            the_category = mongo.db.categories.find_one({"_id" : ObjectId(book_v)})
            if the_category == None:    
                the_category = {
                    "category_name" : "Not assigned yet"
                }
        elif book_k == 'category_id' and book_v == "":
            the_category = {
                "category_name" : "Not assigned yet"
            }
        elif book_k == 'user_id' and book_v != "":
            the_user = mongo.db.users.find_one({"_id" : ObjectId(book_v)})
            if the_user == None:
                the_user = {
                    "username" : "Anonymous"
                }
        elif book_k == 'user_id' and book_v == "":
            the_user = {
                "username" : "Anonymous"
            }
    
    if the_review != None:
        for review_k, review_v in the_review.items():
            if review_k == 'user_id':
                the_reviewer = mongo.db.users.find_one({"_id" : ObjectId(review_v)})
    else:
        the_review = {
            "review" : "Not reviewed yet",
            "date_added" : "Not reviewed yet"
        }
        the_reviewer = {
            "username" : "No reviewer yet"
        }
    
    return render_template("book.html", book=the_book, category=the_category, user=the_user, comments=the_comments, review=the_review, reviewer=the_reviewer, commenters=the_commenters)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    """
    Function to load WTForm for adding book and render to html and add to database
    
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3 
    """
    
    form = AddBookForm()
    
    if form.validate_on_submit():
        flash(f"Book added to site: {form.title.data.title()}!", "success")
        
        book = {
            "title" : form.title.data.lower(),
            "author_fname" : form.author_fname.data.lower(),
            "author_lname" : form.author_lname.data.lower(),
            "category_id" : form.category_id.data,
            "user_id" : form.user_id.data,
            "up_votes" : 0,
            "down_votes" : 0,
            "date_added" : date.today().strftime("%Y/%m/%d"),
            "cover_url" : form.cover_url.data,
            "csrf_token" : form.csrf_token.data 
        }
        
        books = mongo.db.books
        books.insert_one(book)
        
        return redirect(url_for("get_books"))
    else:
        return render_template("addbook.html", form=form, categories=mongo.db.categories.find())


@app.route("/edit_book/<book_id>")
def edit_book(book_id):
    """
    Function to load form for a book review and render to html
    """
    
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    all_categories = mongo.db.categories.find()
    
    return render_template("editbook.html", book=the_book, categories=all_categories)


@app.route("/update_book/<book_id>", methods=["POST"])
def update_book(book_id):
    """
    Function to update database with revised book review information
    """
    
    books = mongo.db.books
    books.update({"_id": ObjectId(book_id)},
    {
        "title" : request.form.get("title"),
        "author_fname" : request.form.get("author_fname"),
        "author_lname" : request.form.get("author_lname"),
        "category_id" : request.form.get("category_id"),
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



"""
Management (CRUD) of reviews collection in database
"""  


@app.route("/check_review_exists/<book_id>")
def check_review_exists(book_id):
    """
    Function to check if a review exists already, if so, then pass back to the get_book page.  If not, proceed to add_review function
    """
    
    a_review=mongo.db.reviews.find_one({"book_id" : book_id})
    
    if a_review != None:
        flash(f"A review already exists for the book", "warning")
        return redirect(url_for('get_book', book_id=book_id))
    else:
        return redirect(url_for("add_review", book_id=book_id))
    
    flash(f"Oops, something went wrong!", "danger")
    return redirect(url_for('get_book', book_id=book_id))


@app.route("/add_review/<book_id>", methods=["GET", "POST"])
def add_review(book_id):
    """
    Function to load WTForm for adding review on book
    
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3 
    """
    
    form = AddReviewForm()
    
    if form.validate_on_submit():
        flash(f"New review uploaded!", "success")
        
        review = {
            "review" : form.review.data,
            "book_id" : book_id,
            "user_id" : form.user_id.data,
            "date_added" : date.today().strftime("%Y/%m/%d"),
            "csrf_token" : form.csrf_token.data 
        }
        
        reviews = mongo.db.reviews
        reviews.insert_one(review)
        
        return redirect(url_for("get_book", book_id=book_id))
        
    else:
        return render_template("addreview.html", form=form, book_id=book_id)
        
    flash(f"Oops, something went wrong!", "danger")
    return redirect(url_for('get_book', book_id=book_id))


"""
Management (CRUD) of categories collection in database
"""


@app.route("/get_categories")
def get_categories():
    """
    Function to fetch categories from database and render to html
    """
    
    return render_template("categories.html", categories=mongo.db.categories.find())


@app.route("/add_category", methods=["GET","POST"])
def add_category():
    """
    Function to load WTForm for adding category and render to html and add to database
    
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3 
    """
    
    if g.user:
        form = CategoryForm()
        if form.validate_on_submit():
            flash(f"New category created: {form.category_name.data}!", "success")
            
            category = {
                "category_name" : form.category_name.data.lower(),
                "cover_url" : form.cover_url.data,
                "csrf_token" : form.csrf_token.data 
            }
            
            categories = mongo.db.categories
            categories.insert_one(category)
            
            return redirect(url_for("get_categories"))
        
        else:
            return render_template("addcategory.html", form=form)
    
    else:
        flash("You need to log in first...", "warning")
        return redirect(url_for("log_user_in"))
   
 
@app.route("/edit_category/<category_id>")
def edit_category(category_id):
    """
    Function to load form for a category to be changed and render to html
    """
    
    the_category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    
    return render_template("editcategory.html", category=the_category)


@app.route("/update_category/<category_id>", methods=["POST"])
def update_category(category_id):
    """
    Function to update database with revised category information
    """
    
    categories = mongo.db.categories
    categories.update({"_id": ObjectId(category_id)},
    {
        "category_name" : request.form.get("category_name")
    })
    
    return redirect(url_for("get_categories"))


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """
    Function to delete a category from the database
    """
    
    mongo.db.categories.remove({"_id" : ObjectId(category_id)})
    
    return redirect(url_for("get_categories"))


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
    
    form = AddCommentForm()
    
    if form.validate_on_submit():
        flash(f"New comment posted!", "success")
        
        comment = {
            "comment" : form.comment.data.lower(),
            "book_id" : book_id,
            "user_id" : form.user_id.data,
            "csrf_token" : form.csrf_token.data 
        }
        
        comments = mongo.db.comments
        comments.insert_one(comment)
        
        return redirect(url_for("get_book", book_id=book_id))
        
    else:
        return render_template("addcomment.html", form=form, book_id=book_id)


"""
Management (CRUD) of users collection in database
"""


@app.route("/get_users")
def get_users():
    """
    Function to fetch users from database and render to html
    """
    
    return render_template("users.html", users=mongo.db.users.find())

def user_exists(search_type, user_detail):
    """
    Function to validate if username or email is already taken in database
    """
    
    the_user = mongo.db.users.find_one({str(search_type): str(user_detail)})
    
    if the_user != None:
        return True
    else:
        return False


@app.route("/add_user", methods=["GET","POST"])
def add_user():
    """
    Function to load WTForm for user registration and render to html, and write to database
    
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
    
    User authentication code adapted from from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=CSHx6eCkmv0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=6
    """
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        print("Username: " + str(form.username.data.lower()))
        
        username_exist = user_exists("username", form.username.data.lower())
        email_exist = user_exists("email", form.email.data.lower())
        if username_exist == True and email_exist == True:
            username_error = "That username already exists.  Please choose a different one..."
            email_error = "That email already exists.  Please choose a different one..."
            return render_template("adduser.html", form=form, username_error=username_error, email_error=email_error)
        elif username_exist == True and email_exist != True:
            username_error = "That username already exists.  Please choose a different one..."
            return render_template("adduser.html", form=form, username_error=username_error)
        elif username_exist != True and email_exist == True:
            email_error = "That email already exists.  Please choose a different one..."
            return render_template("adduser.html", form=form, email_error=email_error)
        
        
        hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        flash(f"Account created for {form.username.data}! You are free to log in...", "success")
        
        user = {
            "fname" : form.fname.data.lower(),
            "lname" : form.lname.data.lower(),
            "email" : form.email.data.lower(),
            "username" : form.username.data.lower(),
            "password" : hash_password,
            "csrf_token" : form.csrf_token.data 
        }
        
        users = mongo.db.users
        users.insert_one(user)
        
        return redirect(url_for("login_user"))
    else:
        
        return render_template("adduser.html", form=form)


#@login_manager.user_loader
#def load_user(user_id):
#    """
#    Function to manage loading of users as part of login_manager
#    
#    Code adapted from Corey Shafer's tutorial found at
#    https://www.youtube.com/watch?v=CSHx6eCkmv0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=6
#    """
#    
#    the_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
#    
#    return the_user 


@app.route("/log_user_in", methods=["GET","POST"])
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
        user = mongo.db.users.find_one({"email" : form.email.data.lower()})
        if user!= None:
            for k, v in user.items():
                if k == "password":
                    if user and bcrypt.check_password_hash(v, form.password.data):
                        session["user"] = str(user["_id"])
                        return redirect(url_for('home_screen'))
                    else:
                        flash(f"Log in unsuccessful!  Check your email and password.", "danger")
        else:
            flash(f"Log in unsuccessful!  Check your email and password.", "danger")
    
    return render_template("loginuser.html", form=form)
    

@app.route("/edit_user/<user_id>")
def edit_user(user_id):
    """
    Function to load form for a user to be editted and render to html
    """
    
    the_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    return render_template("edituser.html", user=the_user)
    

@app.route("/update_user/<user_id>", methods=["POST"])
def update_user(user_id):
    """
    Function to update database with revised user information
    """
    
    users = mongo.db.users
    users.update({"_id": ObjectId(user_id)},
    {
        "fname" : request.form.get("fname"),
        "lname" : request.form.get("lname"),
        "email" : request.form.get("email"),
        "phone" : request.form.get("phone"),
        "username" : request.form.get("username"),
        "password" : request.form.get("password")
    })
    
    return redirect(url_for("get_users"))


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    """
    Function to delete a user from the database, checks whether user is logged
    in and only allows user to delete own account.
    """
    if g.user:
        if g.user == user_id:
            flash("User profile deleted", "success")
            print("Removing user from db")
            #mongo.db.users.remove({"_id" : ObjectId(user_id)})
            return close_session()
            
        else:
            flash("You cannot remove this user, you do not have the relevant privileges...", "danger")
            print("User not removed, not same id")
            return redirect(url_for("get_users"))
    
    else:
        flash("You need to log in first...", "warning")
        return redirect(url_for("log_user_in"))
   
#    return redirect(url_for("get_users"))


@app.route("/get_session")
def get_session():
    """
    Function to check session status
    """
    if "user" in session:
        print("")
        print("##Get Session##")
        print("Session Active: ")
        print(session["user"])
        print("User logged in.")
        return redirect(url_for('home_screen'))
    else:
        print("")
        print("##Get Session##")
        print("Session Not Active: ")
        print(session)
        print("User NOT logged in!")
        return redirect(url_for('home_screen'))

@app.route("/close_session")
def close_session():
    """
    Function to force clossure of session
    """
    session.pop("user", None)
    print("")
    print("##Close Session##")
    print("Session Closed: ")
    print(session)
    print("User logged OUT!")
    return redirect(url_for('home_screen'))


@app.route("/protected")
def protected():
    if g.user:
        return render_template("protected.html")
    flash("You need to log in first...", "warning")
    return redirect(url_for("log_user_in"))

@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

