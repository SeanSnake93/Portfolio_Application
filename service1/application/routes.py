import requests, json
from flask import render_template, request, redirect, url_for, jsonify
from application import app, db, bcrypt
from application.models import Users, Records, Entities, Blocks, Tag_Links, Tags
from application.forms import {{ Inport, Forms, Here }}
from flask_login import login_user, current_user, logout_user, login_required

# source = {Collection:{EntityID{field:value}}, Tables:{table:{field:value}}, User_Tags:{TagID:{field:value}}, Entry_Tags:{TagID:{field:value}}, Tags:{TagID:{field:value}}}
# flags = [Collection, User_Tags, Entry_Tags, Table]

def aquire_datapack(source, flags):
    packet = {}
    for flag in flags:

        if "Collection" in flag:
            flash_beta = Entities.query.filter_by(publisher=int(source[Tables][Users][id])).all()
            for entry in flash_beta:
                wrap += {str(entry.id):{"title":entry.title, "type":entry.type, "publisher":entry.publisher, "day":entry.date_day, "month":entry.date_month, "year":entry.date_year, "time":entry.date_time}}
            packet += {"Entries":wrap}

        elif "User_Tags" in flag:
            flash_alpha = Tag_Links.query.filter_by(referance_user=int(source[Tables][Users][id])).all()
            for entry in flash_alpha:
                flash_beta = Tags.query.filter_by(id=entry.tag_id).first()
                wrap += {str(entry.id):{"tag":flash_beta.tag, "target":flash_beta.target}}
            packet += {"User_Tags":wrap}

        elif "Entry_Tags" in flag:
            flash_alpha = Tag_Links.query.filter_by(referance_user=int(source[Tables][Entries][id])).all()
            for entry in flash_beta:
                flash_beta = Tags.query.filter_by(id=entry.tag_id).first()
                wrap += {str(entry.id):{"tag":flash_beta.tag, "target":flash_beta.target}}
            packet += {"User_Tags":wrap}

        elif "Table" in flag:
            for table in source[Table]:
                flash_alpha = table.query.all()
                for entry in flash_alpha:
                    if source == "Users":
                        wrap += {str(entry.id):{"User_name":entry.User_name , "Email":entry.email, "Record":str(entry.record)}}
                    elif source == "Records":
                        wrap += {str(entry.id):{"first_name":entry.first_name, "middle_name":entry.middle_name, "last_name":entry.last_name, "sex":entry.sex, "dob_day":str(entry.dob_day), "dob_month":str(entry.dob_month), "dob_year":str(entry.dob_year), "sub_day":str(entry.sub_day), "sub_month":str(entry.sub_month), "sub_year":str(entry.sub_year), "sub_time":str(entry.sub_time)}}
                    elif source == "Entries":
                        wrap += {str(entry.id):{"title":entry.title, "type":entry.type, "publisher":str(entry.publisher), "day":str(entry.date_day), "month":str(entry.date_month), "year":str(entry.date_year), "time":str(entry.date_time)}}
                    elif source == "Blocks":
                        wrap += {str(entry.id):{"parent_id":str(entry.parent_id), "has_child":entry.has_child, "tag_id":str(entry.tag_id), "entity_id":str(entry.entity_id), "position":str(entry.position)}}
                    elif source == "Tag_Links":
                        wrap += {str(entry.id):{"user":str(entry.referance_user), "entry":str(entry.referance_entry), "tag":str(entry.tag_id)}}
                    elif source == "Tags":
                        wrap += {str(entry.id):{"tag":entry.tag, "target":entry.target}}
                packet += {table:wrap}

        else:
            print("Flag called {", flag,  "} could not be found")
    return packet

# --- Root Pages Routes --- Start --- >>>

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        source = {"Tables":{"Users":{"user_name":str(current_user.id)}}}
        flag = ["Collection"]
        delivery = aquire_datapack(source, flag)
    return render_template('home.html', datapacket = delivery, title = 'Index')

@app.route('/browse')
def home():
    source = {"Tables":"Entries"}
    flag = ["Table"]
    delivery = aquire_datapack(source, flag)
    if current_user.is_authenticated:
        source = {"Tables":{"Users":{"user_name":str(current_user.id)}}}
        flag = ["Collection"]
        delivery += aquire_datapack(source, flag)
    return render_template('browse.html', datapacket = delivery, title = 'Entries')

# --- Roop Pages Routes -- Finish --- <<<

# --- Entries Routes --- Start --- >>>

@app.route('/portfolio/<publisher>/<title>', methods=['GET','POST'])
def user(publisher, title):
    delivery = aquire_datapack(current_user.user_name, "standard")
    # this will need to be capable of displaying Blocks in order and enable child entities.
    return render_template('entity.html', datapacket = delivery, title = delivery[Table][Entities][entity_title])

@app.route('/portfolio/<publisher>/<title>/edit', methods=['GET','POST'])
def user(publisher, title):
    delivery = aquire_datapack(current_user.user_name, "standard")
    # will need to list all blocks inside this entry and any other details
    return render_template('entity.html', datapacket = delivery, title = 'Edit ~ ' + delivery[Table][Entities][entity_title])

# --- Entries Routes -- Finish --- <<<

# --- User Routes --- Start --- >>>

@app.route('/<user_name>', methods=['GET','POST'])
def user():
    delivery = aquire_datapack(current_user.user_name, "standard, user")
    # will need to list all owned tags and entries
    return render_template('user.html', datapacket = delivery, title = 'Users Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """This function is to process the users details upon registering."""
    if current_user.is_authenticated:
        return redirect(url_for('<user_name>'))
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
        return redirect(url_for('<user_name>'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """This is to allow the user to login"""
    if current_user.is_authenticated:
        return redirect(url_for('<user_name>'))
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
                return redirect(url_for('<user_name>'))
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
        return redirect(url_for('<user_name>'))
    elif request.method =='GET':
        form.first_name =  current_user.first_name
        form.middle_name =  current_user.middle_name
        form.last_name = current_user.last_name
    delivery = aquire_datapack()
    return render_template('user_edit.html', datapacket = delivery, title='Account Page', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Clicking the Logout button on the menu will Log the user
    out of the site."""
    logout_user()
    return redirect(url_for('home'))

# --- User Routes -- Finish --- <<<