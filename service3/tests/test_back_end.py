import unittest
from flask import abort, url_for
from flask_testing import TestCase
from application import app, db, bcrypt
from application.models import Users, Films, Collection
from os import getenv

# ---------- Base-SetUp-Testing ----------

class TestBase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app.config.update(
            SQLALCHEMY_DATABASE_URI=getenv('TEST_CROSSWAVE_URI'),
            SECRET_KEY=getenv('TEST_STUDIO_KEY'),
            WTF_CSRF_ENABLED=False,
            DEBUG=True
            )
        return app

    def setUp(self):
        """Will be called before every test"""
        db.drop_all()
        db.create_all()
        db.session.commit()
        hashed_pw1 = bcrypt.generate_password_hash('Adm1nSy5temT35t1n8')
        admin_user = Users(
            user_name="Admin",
            email="AdminSystem@Testing.com",
            password=hashed_pw1,
            record=1
            )
        admin_details = Users(
            first_name="Admin",
            middle_name="System",
            last_name="Testing",
            sex = "Male",
            dob_day = 1,
            dob_month = 1,
            dob_year = 2000,
            sub_day = 1,
            sub_month = 1,
            sub_year = 2020,
            sub_time = 00:00
            )
        hashed_pw_2 = bcrypt.generate_password_hash('Sy5temT35t1n8')
        employee = Users(
            user_name="Employee",
            email="System@Testing.com",
            password=hashed_pw_2,
            record=2
            )
        employee_details = Users(
            first_name="Employee",
            middle_name="System",
            last_name="User",
            sex = "Female",
            dob_day = 5,
            dob_month = 1,
            dob_year = 2000,
            sub_day = 5,
            sub_month = 1,
            sub_year = 2020,
            sub_time = 00:00
            )
        entity1 = Entities(
            title="Employee",
            type="System",
            publisher="User",
            date_day = 5,
            date_month = 1,
            date_year = 2000,
            date_time = 00:00
            )
        block11 = Blocks(
            parent_id="",
            has_child=False,
            tag_id=1
            entity_id=1
            position=1
        )
        block12 = Blocks(
            parent_id="",
            has_child=False,
            tag_id=2,
            entity_id=1,
            position=2
        )
        entity2 = Entities(
            title="Employee",
            type="System",
            publisher="User",
            date_day = 5,
            date_month = 1,
            date_year = 2000,
            date_time = 00:00
            )
        block21 = Blocks(
            parent_id="",
            has_child=False,
            tag_id=3,
            entity_id=2,
            position=1
        )
        tag1 = Tags(
            tag="text",
            target="This is to be propper content at some point."
        )
        tag2 = Tags(
            tag="text",
            target="But as a team we will try and try again."
        )
        tag3 = Tags(
            tag="text",
            target="Untill the day it is finaly finished."
        )
        tag_link1 = Tag_Links(
            referance_user="",
            referance_entry=1,
            tag_id=1
        )
        tag_link2 = Tag_Links(
            referance_user="",
            referance_entry=2,
            tag_id=2
        )
        tag_link3 = Tag_Links(
            referance_user="",
            referance_entry=2,
            tag_id=3
        )
        db.session.add(admin_details)
        db.session.add(admin)
        db.session.add(employee_details)
        db.session.add(employee)
        db.session.add(entity1)
        db.session.add(block11)
        db.session.add(block12)
        db.session.add(entity2)
        db.session.add(block21)
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.add(tag_link1)
        db.session.add(tag_link2)
        db.session.add(tag_link3)
        db.session.commit()

    def tearDown(self):
        """Will be called after every test"""
        db.session.remove()
        db.drop_all()

# -------- END-Base-SetUp-Testing --------

# ____________________________________________________________________

# ---------- Visit-Testing ----------

class TestViews(TestBase):
    def test_homepage_view(self):
        """This is the server getting a status code 200"""
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

# -------- END-Visit-Testing --------