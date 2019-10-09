"""
Code adapted for use of WTForms in site from WTForms Documentation at 
https://wtforms.readthedocs.io/en/stable/index.html 

and 

Corey Shafer tutorial found at
https://www.youtube.com/watch?v=UIJKdCIEXUQ&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=3
"""

"""
Imports of packages for functioning of forms for the site
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
"""
Form classes for various forms used
"""

class RegistrationForm(FlaskForm):
    fname = StringField("First Name",
                        validators=[DataRequired(), Length(min=1)])
    lname = StringField("Surname", 
                        validators=[DataRequired(), Length(min=1)])
    email = StringField("Email", 
                        validators=[DataRequired(), Email()])
    phone = StringField("Phone", 
                        validators=[DataRequired()])
    username = StringField("Username", 
                            validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField("Password", 
                            validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField("Confirm Password", 
                            validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")
                            

