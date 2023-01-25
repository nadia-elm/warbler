

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class TestMessageModel(TestCase):
    def setUp(self):
        """Create test client , add sample data"""
        db.drop_all()
        db.create_all()
        self.id = 111
        testuser = User.signup("testuser","test@test.com", "testpassword", "testimage.jpg")
        testuser.id = self.id
        db.session.commit()

        


        def tearDown(self):
            # delete the test database
           res = super().tearDown()
           db.session.rollback()
           return res
        

        def test_message_model(self):
            testmessage = Message(text="test message", user_id = self.testuser.id)
            db.session.add(testmessage)
            db.session.commit()

            self.assertEqual(len(self.testuser.messages), 1)
            self.assertEqual(self.testuser.messages[0].text, "test message")


