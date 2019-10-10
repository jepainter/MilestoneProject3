"""
Imports of packages for functioning of site
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm, LogInForm, AddBookForm, AddCategoryForm, AddCommentForm

app = Flask(__name__)

MONGODB_URI = os.getenv("MONGO_URI")

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


mongo = PyMongo(app)

@app.route("/", methods=["GET", "POST"])
@app.route("/home_screen", methods=["GET", "POST"]) #remove this if not necessary, test first
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
    #    print("specific category given")
    elif category_id == "":
        books=mongo.db.books.find()
    #    print("no category given")
    
    
    #Populate new dictionary with results from db retrieval
    for book in books:
        for key, value in book.items():
            if key == "_id":
                merged_result[str(value)] = book
    
    #Update new dictionary with category and user information
    for book_id, book_detail in merged_result.items():
        for key, value in book_detail.items():
            if key == "category_id":
                the_category=mongo.db.categories.find_one({"_id": ObjectId(value)})
                merged_result[book_id]["category_name"] = merged_result[book_id].pop("category_id")
                for k, v in the_category.items():
                    if k == "category_name":
                        merged_result[book_id]["category_name"] = the_category[k]    
            elif key == "user_id":
                the_user=mongo.db.users.find_one({"_id": ObjectId(value)})
                merged_result[book_id]["username"] = merged_result[book_id].pop("user_id")
                for k, v in the_user.items():
                    if k == "username":
                        merged_result[book_id]["username"] = the_user[k]
            else:
                pass
    
    return render_template("books.html", books=merged_result, categories=mongo.db.categories.find())

@app.route("/get_book/<book_id>")
def get_book(book_id):
    """
    Function to get individual book details and render to html
    """
    the_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    all_categories = mongo.db.categories.find()
    all_users = mongo.db.users.find()
    all_comments = mongo.db.comments.find()
    
    return render_template("book.html", book=the_book, categories=all_categories, users=all_users, comments=all_comments)

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
   #     print("Add Book Function>")
    #    print("Form validation success")
     #   print("Errors: " + str(form.errors))
      #  print("Form data: " + str(form.title.data))
        
        book = {
            "title" : form.title.data.lower(),
            "author_fname" : form.author_fname.data.lower(),
            "author_lname" : form.author_lname.data.lower(),
            "category_id" : form.category_id.data,
            "user_id" : form.user_id.data,
            "up_votes" : 0,
            "down_votes" : 0,
            "cover_url" : form.cover_url.data,
            "csrf_token" : form.csrf_token.data 
        }
        
        #print(book)
        
        books = mongo.db.books
        books.insert_one(book)
        
        return redirect(url_for("get_books"))
    else:
    #    print("Add Book Function>")
    #    print("Form validation unsuccessful")
    #    print("Errors: " + str(form.errors))
    #    print("Form: " + str(form))
        return render_template("addbook.html", form=form, categories=mongo.db.categories.find())

    #old code below
    #form = AddBookForm()
    #if form.validate_on_submit():
    #    flash(f"Book added to site!", "success")
    #    return redirect(url_for("get_books"))
    #return render_template("addbook.html", form=form, categories=mongo.db.categories.find())
    #end of old code

######## 
#remove this function, no longer required
#@app.route("/insert_book", methods=["POST"])
#def insert_book():
#    """
#    Function to insert a book into the database
#    """
#    books = mongo.db.books
#    books.insert_one(request.form.to_dict())
#    return redirect(url_for("get_books"))
#########


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
    Function to update database with revised book review information
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
    
    form = AddCategoryForm()
    
    if form.validate_on_submit():
        flash(f"New category created: {form.category_name.data}!", "success")
        print("Add Category Function>")
        print("Form validation success")
        print("Errors: " + str(form.errors))
        print("Form data: " + str(form.category_name.data))
        
        category = {
            "category_name" : form.category_name.data.lower(),
            "cover_url" : form.cover_url.data,
            "csrf_token" : form.csrf_token.data 
        }
        
        print(category)
        
        categories = mongo.db.categories
        categories.insert_one(category)
        
        return redirect(url_for("get_categories"))
    else:
        print("Add Category Function>")
        print("Form validation unsuccessful")
        print("Errors: " + str(form.errors))
        print("Form: " + str(form))
        return render_template("addcategory.html", form=form)
    
    """
    old code, remove
    form = AddCategoryForm()
    if form.validate_on_submit():
        flash(f"Category added to site!", "success")
        return redirect(url_for("get_categories"))
    return render_template("addcategory.html", form=form)
    end of old code
    """
##########
#remove function not required anymore
#@app.route("/insert_category", methods=["POST"])
#def insert_category():
#    """
#    Function to insert a category into the database
#    """
#    categories = mongo.db.categories
#    categories.insert_one(request.form.to_dict())
#    return redirect(url_for("get_categories"))
###########


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
    the_book = mongo.db.books.find_one({"_id" : ObjectId(book_id)})
    if form.validate_on_submit():
        flash(f"Comment added for book!", "success")
        return redirect(url_for("get_book(book_id)"))
    return render_template("addcomment.html", form=form, book=the_book)

@app.route("/insert_comment/<book_id>", methods=["POST"])
def insert_comment(book_id):
    """
    Function to insert a comment into the database
    """
    
    comment = request.form.to_dict()
    comment["book_id"] = book_id
    
    comments = mongo.db.comments
    comments.insert_one(comment)
    
    return redirect(url_for('get_book', book_id=book_id))


"""
Management (CRUD) of users collection in database
"""
@app.route("/get_users")
def get_users():
    """
    Function to fetch users from database and render to html
    """
    return render_template("users.html", users=mongo.db.users.find())


@app.route("/add_user", methods=["GET","POST"])
def add_user():
    """
    Function to load WTForm for user registration and render to html, and write to database
    
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3 
    """
    form = RegistrationForm()
    
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        #print("Add User Function>")
        #print("Form validation success")
        #print("Errors: " + str(form.errors))
        #print("Form data: " + str(form.username.data))
        
        user = {
            "fname" : form.fname.data.lower(),
            "lname" : form.lname.data.lower(),
            "email" : form.email.data.lower(),
            "username" : form.username.data.lower(),
            "password" : form.password.data,
            "csrf_token" : form.csrf_token.data 
        }
        
        #print(user)
        
        users = mongo.db.users
        users.insert_one(user)
        
        return redirect(url_for("home_screen"))
    else:
        #print("Add User Function>")
        #print("Form validation unsuccessful")
        #print("Errors: " + str(form.errors))
        #print("Form: " + str(form))
        return render_template("adduser.html", form=form)

#####################
# remove insert function below, as it is dealt with through the add user function
#@app.route("/insert_user/<form>", methods=["GET","POST"])
#def insert_user(form):
#    """
#    Function to insert a new user into the database
#    """
#    #user={
#    #    "username" : form.username.data,
#    #    "fname" : form.fname.data,
#   #    "lname" : form.lname.data,
#    #    }
#    
#    #users = mongo.db.users
#    #users.insert_one(user)
#    print("Insert User Function>")
#    print("Form data: " + str(form.username.data))
#    for field in form:
#        print(str(field))
#    #print("User: " + str(user))
#    
#    return redirect(url_for("home_screen"))
####################


@app.route("/login_user", methods=["GET", "POST"])
def login_user():
    """
    Function to load WTForm for user log in and render to html
    
    WTForms code adapted from Corey Shafer's tutorial found at
    https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3 
    """
    form = LogInForm()
    if form.validate_on_submit():
        flash(f"Log in successful!", "success")
        return redirect(url_for("home_screen"))
    else:
        flash(f"Log in unsuccessful!", "danger")
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
    Function to delete a user from the database
    """
    mongo.db.users.remove({"_id" : ObjectId(user_id)})
    return redirect(url_for("get_users"))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

