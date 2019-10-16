"""
Code adapted for use of WTForms in site from WTForms Documentation at 
https://wtforms.readthedocs.io/en/stable/index.html 

and with help from

Corey Shafer's tutorial found at
https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
"""

"""
Imports of packages for functioning of forms for the site
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

"""
Form classes for various forms used
"""

class RegistrationForm(FlaskForm):
    """
    Form to capture and validate registration of users
    """
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2)])
    lname = StringField("Surname", validators=[DataRequired(), Length(min=2)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    

class LogInForm(FlaskForm):
    """
    Form to capture and validate log in of users
    """
    email = StringField("Email", 
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password", 
                            validators=[DataRequired(), Length(min=8, max=16)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class BookForm(FlaskForm):
    """
    Form to capture and validate new book to add as  well as update book info
    
    up_votes and down_votes and date_added are set within the add_book function
    """
    title = StringField("Title:", 
                        validators=[DataRequired(), Length(min=1)])
    author_fname = StringField("Author First Name", 
                                validators=[DataRequired(), Length(min=1)])
    author_lname = StringField("Author Surname", 
                                validators=[DataRequired(), Length(min=1)])
    category_id = StringField("Category")
    cover_url = StringField("Cover Link", 
                                validators=[DataRequired(), Length(min=2)])
    

class CategoryForm(FlaskForm):
    """
    Form to capture and validate new category to add, as well as used to update
    categories
    """
    category_name = StringField("Category Name", 
                            validators=[DataRequired(), Length(min=2)])
    cover_url = StringField("Cover Link", 
                            validators=[DataRequired(), Length(min=2)])
    

class AddCommentForm(FlaskForm):
    """
    Form to capture and validate new comment to add
    
    book_id is assigned within the function add_book
    """
    comment = StringField("Comment", validators=[DataRequired(), Length(min=2, max=140)])
    user_id = StringField("UserId", validators=[DataRequired(), Length(min=10)])


class AddReviewForm(FlaskForm):
    """
    Form to capture and validate new review to add
    
    book_id is assigned within the function add_review
    """
    review = StringField("Review", validators=[DataRequired(), Length(min=10, max=1000)])
    user_id = StringField("UserId", validators=[DataRequired(), Length(min=10)])