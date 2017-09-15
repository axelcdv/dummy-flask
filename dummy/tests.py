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
        # with app.app_context():
            response = self.client.get('/users/123/')
            assert response.status_code == 404
            user = UserFactory()
            # db.session.commit()
            response = self.client.get('/users/{}/'.format(user.id))
            assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()
