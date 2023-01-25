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

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        self.test_user1 = User.signup("testuser1", "test1@test.com", "testpassword1", "testimage1.jpg")
        self.test_user2 = User.signup("testuser2", "test2@test.com", "testpassword2", "testimage2.jpg")

        db.session.add(self.test_user1)
        db.session.add(self.test_user2)

        db.session.commit()


        self.assertEqual(len(self.test_user1.messages), 0)
        self.assertEqual(len(self.test_user1.followers), 0)
        self.client = app.test_client()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    

    def test_user_signup(self):
        # test that a user is successfully added to the database
        user = User.query.filter_by(username = "testuser1").first()
        self.assertEqual(user.username , "testuser1")
        self.assertEqual(user.email, "test1@test.com")
        self.assertEqual(user.image_url, "testimage1.jpg")



    def test_user_authenticate(self):
        # test that a user can be authenticated
        authenticated_user = User.authenticate("testuser1", "testpassword1")
        self.assertEqual(authenticated_user.username , "testuser1")

    def test_user_authenticate_fails(self):
        authenticated_user = User.authenticate("testuser1", "wrongpassword")
        self.assertFalse(authenticated_user)

    def test_is_following(self):
        self.test_user1.following.append(self.test_user2)
        db.session.commit()

        self.assertTrue(self.test_user1.is_following(self.test_user2))
        self.assertFalse(self.test_user2.is_following(self.test_user1))

    def test_is_followed_by(self):
        self.test_user1.following.append(self.test_user2)
        db.session.commit()

        self.assertTrue(self.test_user2.is_followed_by(self.test_user1))
        self.assertFalse(self.test_user1.is_followed_by(self.test_user2))


    def test_login(self):
        # test that a user can successfully log in
        with self.client:
            response = self.client.post('/login',
                                         data={"username" : "testuser1",
                                                "password" : "testpassword1"}
                                                  ,follow_redirects = True)
               
               
          
            self.assertEqual(response.status_code, 200)





        

