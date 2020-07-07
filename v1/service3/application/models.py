from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

# --- User Models --- Start --- >>>

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True) # No Spaces allowed
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False, unique=True) # Encrypted
    record = db.Column(db.Integer, db.ForeignKey('Records.id'), nullable=False) # Links to Users details
    tag_links = db.relationship('Tags_Links', backref='tags', lazy=True) # Tags table holds all referanced 'tag' data and target data i.e. Images, Web Links and Display content
    
    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Known As: ', self.user_name, '\r\n',
            'Email: ', self.email,'\r\n',
            'Record Number: ', self.record
        ])

class Records(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False, unique=False)
    middle_name = db.Column(db.String(30), nullable=True, unique=False)
    last_name = db.Column(db.String(30), nullable=False, unique=True)
    sex = db.Column(db.String(10), nullable=False, unique=False) # Male / Female
    dob_day = db.Column(db.Integer, nullable=False) # Date of Birth
    dob_month = db.Column(db.Integer, nullable=False)
    dob_year = db.Column(db.Integer, nullable=False)
    sub_day = db.Column(db.Integer, nullable=False) # Date the user subscribed to the application
    sub_month = db.Column(db.Integer, nullable=False)
    sub_year = db.Column(db.Integer, nullable=False)
    sub_time = db.Column(db.Integer, nullable=False)
    referenced_in_user = db.relationship('Users', backref='Users_Record', lazy=True) # Refurs to the Users Table
    
    def __repr__(self):
        return ''.join([
            'Name: ', self.first_name, self.middle_name,  self.last_name, '\r\n',
            'Sex: ' , self.sex, '\r\n',
            'D.O.B: ' , str(self.dob_day), '/', str(self.dob_month), '/', str(self.dob_year),
            'Subscribed: ', str(self.sub_day), '/', str(self.sub_month), '/', str(self.sub_year) ' @ ', str(self.sub_time)
        ])

# --- User Models -- Finish --- <<<

# --- Portfolio Models --- Start --- >>>

class Entities(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=False) # Title for the entry
    type = db.Column(db.String(16), nullable=False, unique=False) # This is to be used to set the template for the thumbnail
    publisher = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # User who made the entry
    date_day = db.Column(db.Integer, nullable=False) # Date it was created
    date_month = db.Column(db.Integer, nullable=False)
    date_year = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.Integer, nullable=False)
    tag_links = db.relationship('Tag_Links', backref='tags', lazy=True) # Any Tags linked to this entry i.e. Images, Web Links and Display content

    def __repr__(self):
        return ''.join([
            'Entity ID: ', str(self.id), '\r\n',
            'Title: ', str(self.parent_id), '\r\n',
            'Type: ', str(self.type), '\r\n',
            'Publisher: ', str(self.publisher), '\r\n',
            'Published: ', str(self.date_day), '/', str(self.date_month), '/', str(self.date_year) ' @ ', str(self.date_time)
        ])

class Blocks(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('blocks.id'), nullable=True) # If this block is to sit inside another then the block is to referance its parent.
    has_child = db.Column(db.Boolian, nullable=False) # This is a True of False that is to be refured to in the HTML as to display spesific fields.
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=True) # The Tag_id refures to a 'tag' called Content. This is to be displayed on the page only if has_child is False
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False) # What entity the block belongs to
    position = db.Column(db.Integer, nullable=False) # What possition it belongs in when filtered on the page

    def __repr__(self):
        return ''.join([
            'Block ID: ', str(self.id), '\r\n',
            'Parent Block: ', str(self.parent_id), '\r\n',
            'Parent: ', str(self.has_child), '\r\n',
            'Tag ID: ', str(self.tag_id), '\r\n',
            'Entity ID: ', str(self.entity_id), '\r\n',
            'Position: ', str(self.position)
        ])

# --- Portfolio Models -- Finish --- <<<

# --- Tags Models --- Start --- >>>

class Tag_Links(db.Model):

    id = db.Column(db.Integer, primary_key=True) # This referanses Enrty and User data held as Tags
    referance_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # This Allows the user to pull Links to their page with referanced Tags i.e Social Media
    referance_entry = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=True)  # This Allows the Entity to pull Links to their page with referanced Tags i.e Links to cheacked baised on the thumbnail template.
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False) # Referance to the Tags Table

    def __repr__(self):
        return ''.join([
            'Social ID: ', str(self.id), '\r\n',
            'User ID: ', str(self.referance_user), '\r\n',
            'Entry ID: ', str(self.referance_entry), '\r\n',
            'Tag ID: ', str(self.tag_id)
        ])

class Tags(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20), nullable=False, unique=False) # When sending all the tags back through the other services the data will need to exist within a dictionary, This tag will be how each rederanced
    target = db.Column(db.String(1000), nullable=False, unique=False) # The Image link, Web Link or Block Content
    tags_links = db.relationship('Tags_Links', backref='tags', lazy=True) # Referancing the Tag_Links to Users and Entries

    def __repr__(self):
        return ''.join([
            'Tag ID: ', str(self.id), '\r\n',
            'Tag: ', self.tag, '\r\n',
            'Target: ', self.target
        ])

# --- Tags Models -- Finish --- <<<