from datetime import date, time, datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, BooleanField, TextAreaField, Form, FormField
from flask_sqlalchemy import SQLAlchemy
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from application import app, db
from application.models import Users, Records, Entities, Blocks, Tag_Links, Tags
from flask_login import current_user

class EntityForm(Form):
    
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=100)])
    type = StringField("Entity Type", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Save')
    # Aditional tags will be included to hold the thumbnail and project links

class Con1Form(FlaskForm):

    content1 = TextAreaField("TextBox - 1000", validators=[DataRequired(), Length(min=1, max=1000)])
    # This will only show if the user is not uploading an Image. If they are, then a tag will show instead.

class Con2Form(FlaskForm):

    content2 = TextAreaField("TextBox - 500", validators=[DataRequired(), Length(min=1, max=500)])
    # Refer to line 21

class Con3Form(FlaskForm):

    content3 = TextAreaField("TextBox - 250", validators=[DataRequired(), Length(min=1, max=250)])
    # Refer to line 21

class TagsForm(Form):
    tag = StringField("Tag", validators=[DataRequired(), Length(min=1, max=20)]) # This will be coded in by us to use, view comment bellow.
    target = StringField("Target", validators=[DataRequired(), Length(min=1, max=1000)]) # Web Link or Content
    # i.e. Users { Thumbnail, Links, Social { LinkedIn, Facebook, Twiter, Instagram, Behance}}, Entity{Thumbnail, Content, Image, Links}, Block{Thumbnail, Content, Image, Links}

class UserLoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired(), Length(min=8, max=50)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UserRegisterForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    user_name = StringField("User Name", validators=[DataRequired(), Length(min=5, max=50)])
    password = StringField("Password", validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = StringField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
   
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=1, max=50)])
    middle_names = StringField("Middle Name(s)", validators=[Length(min=1, max=50)])
    surname = StringField("Surname", validators=[DataRequired(), Length(min=1, max=50)])
    sex = StringField("Sex", validators=[DataRequired(), Length(min=2, max=10)])
    day = IntegerField("Day", validators=[DataRequired()])
    month = IntegerField("Month", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])

    submit = SubmitField('Register')

class UserUpdateForm(FlaskForm):

    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    middle_names = StringField("Middle Name(s)", validators=[Length(min=2, max=50)])
    surname = StringField("Surname", validators=[DataRequired(), Length(min=2, max=50)])
    sex = StringField("Sex", validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Confirm')