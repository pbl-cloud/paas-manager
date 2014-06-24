import unittest
import os

os.environ['PAAS_MANAGER_ENV'] = 'test'

from paas_manager.app.models.users import Users


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.user = Users.create({'email': 'test@test', 'password': 'test'})

    def tearDown(self):
        Users.remove_all()

    def test_exists(self):
        self.assertTrue(Users.exists({'email': 'test@test'}))
        self.assertFalse(Users.exists({'email': 'test@testbar'}))

    def test_authorize_success(self):
        user = Users.authorize(self.user.email, 'test')
        self.assertEqual(user.id, self.user.id)

    def test_authorize_fail(self):
        user = Users.authorize('test@test', 'wrong_password')
        self.assertFalse(user)

    def test_count(self):
        self.assertEqual(1, Users.count())

    def test_create(self):
        self.assertEqual(1, Users.count())
        user = Users.create({'email': 'foobar@bar.baz'})
        self.assertIsNotNone(user.id)
        self.assertEqual(2, Users.count())

    def test_find_by(self):
        user = Users.find_by({'email': 'test@test'})
        self.assertEqual('test@test', user.email)

    def test_simple_update_user(self):
        user = Users.create({'email': 'foo@bar'})
        self.assertEqual('foo@bar', user.email)
        user.email = 'foo@baz'
        user.save()
        self.assertEqual('foo@baz', user.email)

    def test_update_user(self):
        user = Users.create({'email': 'bar@bar'})
        user.update({'email': 'foo@baz'})
        user.save()
        self.assertEqual('foo@baz', user.email)


if __name__ == '__main__':
    unittest.main()
