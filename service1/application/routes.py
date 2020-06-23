import requests, json
from flask import render_template, request, redirect, url_for, jsonify
from application import app#, bcrypt, db
from application.models import Users, Records, Entities, Blocks, Tag_Links, Tags
#from application.forms import {{ Inport, Forms, Here }}
from flask_login import login_user, current_user, logout_user, login_required

# --- Root Pages Routes --- Start --- >>>

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home Page')

# --- Roop Pages Routes -- Finish --- <<<

# --- Entries Routes --- Start --- >>>

@app.route('/portfolio/<user_name>/<entity_title>', methods=['GET','POST'])
def user_entity():
    # this will need to be capable of displaying Blocks in order and enable child entities.
    return render_template('entity.html', variable = value, title = 'Users Page')

@app.route('/portfolio/<user_name>/<entity_title>/edit', methods=['GET','POST'])
def user_entity_edit():
    # will need to list all blocks inside this entry and any other details
    return render_template('entity.html', variable = value, title = 'Users Page')

# --- Entries Routes -- Finish --- <<<

# --- User Routes --- Start --- >>>

@app.route('/<user_name>', methods=['GET','POST'])
def user(user_name):
    # will need to list all owned tags and entries
    return render_template('user.html', variable = value, title = 'Users Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """This function is to process the users details upon registering."""
    if current_user.is_authenticated:
        return redirect(url_for('user', user_name = current_user.user_name))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw=bcrypt.generate_password_hash(form.password.data)
        record=Records(
            first_name=form.first_name.data,
            irst_name=form.middle_name.data,
            last_name=form.last_name.data,
            sex=form.sex.data,
            dob_day=form.dob_day,
            dob_month=form.dob_month,
            dob_year=form.dob_year,
            sub_day=form.sub_day,
            sub_month=form.sub_month,
            sub_year=form.sub_year,
            sub_time=form.sub_time
        )
        db.session.add(record)
        db.session.commit()
        link_account = Records.query.last()
        user=Users(
            display_name=form.display_name,
            email=form.email.data, 
            password=hash_pw,
            record=link_account.id
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user', user_name = current_user.user_name))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """This is to allow the user to login"""
    if current_user.is_authenticated:
        return redirect(url_for('user', user_name = current_user.user_name))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(
                user,
                remember=form.remember.data
            )
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('user', user_name = current_user.user_name))
    return render_template('login.html', title='Login Page', form=form)

@app.route('/<user_name>/edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    """This will allow the user to edit their details"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.middle_name = form.middle_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('user', user_name = current_user.user_name))
    elif request.method =='GET':
        form.first_name =  current_user.first_name
        form.middle_name =  current_user.middle_name
        form.last_name = current_user.last_name
    return render_template('user_edit.html', title='Account Page', form=form)

# --- User Routes -- Finish --- <<<