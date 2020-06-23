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
        db.session.add(admin_details)
        db.session.add(admin)
        db.session.add(employee_details)
        db.session.add(employee)
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