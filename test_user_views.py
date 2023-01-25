

import os
from unittest import TestCase

from models import db, connect_db, Message, User, Likes, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class UserViewsTestCase(TestCase):
    """tests for views for pets"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        
       
        self.test_user1 = User.signup("testuser1", "test1@test.com", "testpassword1", "testimage1.jpg")
        self.test_user2 = User.signup("testuser2", "test2@test.com", "testpassword2", "testimage2.jpg")

        db.session.add(self.test_user1)
        db.session.add(self.test_user2)

        db.session.commit()


    def tearDown(self):
        """clean up any transactions"""
        db.session.rollback()


    def test_users_index(self):
        with self.client as client :
            res = client.get('/users')

            self.assertIn("testuser1",str(res.data))
            self.assertIn("testuser2", str(res.data))


    def test_users_search(self):

         with self.client as client :
            res = client.get('/users?q=test')

            self.assertIn("testuser1",str(res.data))
            self.assertIn("testimage2", str(res.data))

            self.assertNotIn("ertyu", str(res.data))


    def test_users_show(self):
        with self.client as client :
            res = client.get(f"/users/{self.testuser1_id}")
            self.assertEqual(res.status_code , 200)
            self.assertIn("testuser1",str(res.data))

            



        


   

@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    # snagging messages in order from the database;
    # user.messages won't be in order by default
    messages = (Message
                .query
                .filter(Message.user_id == user_id)
                .order_by(Message.timestamp.desc())
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, messages=messages)

