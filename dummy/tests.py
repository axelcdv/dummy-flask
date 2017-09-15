import unittest
import factory
import factory.fuzzy
from factory.alchemy import SQLAlchemyModelFactory
from .app import db, User, app


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db.session
        model = User

    username = factory.fuzzy.FuzzyText()
    email = factory.fuzzy.FuzzyText()


class TestUserViews(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_user_list(self):
        with app.app_context():
            response = self.client.get('/users/')
            assert response.status_code == 200

    def test_user_detail(self):
        with app.test_request_context():
            # Make sure requesting an unknown user returns a 404
            response = self.client.get('/users/123/')
            assert response.status_code == 404

            # Create a user
            user = UserFactory()
            db.session.commit()
            response = self.client.get('/users/{}/'.format(user.id))
            assert response.status_code == 200 # This works since the write was committed

    def test_user_uncommitted(self):
        with app.test_request_context():
            # Create a user
            uncommitted_user = UserFactory()
            assert uncommitted_user in db.session
            response = self.client.get('/users/{}/'.format(uncommitted_user.id))
            assert response.status_code == 200 # This doesn't work, the session wasn't reused

