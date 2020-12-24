from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """ Tests for views for Users """

    def setUp(self):
        """ Add Sample user """

        User.query.delete()

        user = User(first_name="TestFirst", last_name="TestLast", image_url="https://images.unsplash.com/photo-1522521612083-730fb19791c1?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1351&q=80")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """ Clean up any fouled transaction """

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h5>TestFirst TestLast</h5>', html)
            self.assertIn(self.user.first_name, html)
    
    def test_add_user(self):
        with app.test_client() as client:
            new_user = {'first_name': 'TestFirst2' , 'last_name': 'TestLast2', 'photo': 'https://images.unsplash.com/photo-1557431518-1f8e3d83c2b0?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80'}
            resp = client.post('/users/new', data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h5>TestFirst2 TestLast2</h5>', html)

    def test_delete_user(self):
        with app.test_client() as client:
            user = User(first_name="TestFirst3", last_name="TestLast3", image_url="https://images.unsplash.com/photo-1570481662006-a3a1374699e8?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mnx8ZG9scGhpbnxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=60")
            db.session.add(user)
            resp = client.post(f'/users/{self.user_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)