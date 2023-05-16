"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        # User.query.delete()
        # Message.query.delete()
        # Follows.query.delete()

        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None, None, "Winamac", "I grew up in a town named after Indians.")
        uid1 = 39
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password", None, None, "Star City", None)
        uid2 = 48
        u2.id = uid2
        
        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2


        self.client = app.test_client()

    def tearDown(self):
        """Clean up at the end of each task/function"""
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 0)
        self.assertEqual(self.u1.email, "email1@email.com")
        self.assertEqual(self.u1.username, "test1")
        self.assertEqual(self.u1.location, "Winamac")
        self.assertEqual(self.u1.bio, "I grew up in a town named after Indians.")

    def test_user_method__repr__(self):
        """This checks if __repr__ will print correctly"""

        self.assertEqual(self.u1.__repr__(), f"<User #{39}: test1, email1@email.com>")
        self.assertEqual(self.u2.__repr__(), f"<User #{48}: test2, email2@email.com>")

    def test_user_method_is_followed_by(self):

        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))
    
    def test_user_method_is_following(self):

        self.u1.followers.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_following(self.u1))
        self.assertFalse(self.u1.is_following(self.u2))
    
    def test_user_signup(self):
        u_test = User.signup("user3", "user3@email.com", "password", None, None, None)
        uid = 9999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "user3")
        self.assertEqual(u_test.email, "user3@email.com")
        self.assertNotEqual(u_test.password, "password")
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
        
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))
    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

