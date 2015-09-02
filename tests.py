import types
import seed
import datetime
import unittest
import requests
import tempfile
import json
import os
import flask
from model import connect_to_db, db, Experience, User, Booked, Provider, Wanderlist, Category, Venue
from server import app
import seed


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_filename = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + self.db_filename
        app.config['TESTING'] = True
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.test_client = app.test_client()
        db.app = app
        db.init_app(app)
        with app.app_context():
            db.create_all()
        seed.load_categories()
        seed.load_providers()
        seed.load_venues()
        seed.load_experiences()

    def login(self, client):
        """submit login info"""
        return client.post('/login', data=dict(email="jessica.a.lopez@yale.edu",password="andiamo"), follow_redirects=True)

    def test_login(self):
        """login adds user_id to session"""
        with app.test_client() as c:
            self.login(c)
            assert flask.session['user_id'] == 1

    def test_database_seed(self):
        """Ensure that the database seed file functions as expected."""

        user = User.query.get(1)
        experience = Experience.query.get(1)
        assert user.user_email == "jessica.a.lopez@yale.edu"
        assert experience.exp_name == "Golden Gate Seaplane Tour"

    def test_no_route(self):
        """test that a user gets a 404 error when trying to access a nonexistant route."""

        response = self.test_client.get('/thisdoesntexist')
        assert response.status_code == 404

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_filename)

if __name__ == '__main__':
    from server import app
    from model import connect_to_db
    connect_to_db(app)
    unittest.main()