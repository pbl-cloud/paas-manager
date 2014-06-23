import unittest
import os

os.environ['PAAS_MANAGER_ENV'] = 'test'

from paas_manager.app.models.users import Users

class TestUsers(unittest.TestCase):
    users = Users()

    def setUp(self):
        Users.register_user('test@test', 'test')

    def tearDown(self):
        Users.remove_all()

    def test_is_registered(self):
        self.assertTrue((Users.is_registered('test@test')))

    def test_verify_success(self):
        self.assertEqual(Users.verify_password('test@test', 'test'), self.users.user_id('test@test'))

    def test_verify_failed(self):
        self.assertEqual(Users.verify_password('test@test', 'pass'), None)

    def test_create(self):
        self.assertEqual(1, len(Users.find()))
        user = Users.create({'email': 'foobar@bar.baz'})
        self.assertIsNotNone(user.id)
        self.assertEqual(2, len(Users.find()))

    def test_user_id(self):
        id = Users.user_id('test@test')

    def test_find_by(self):
        user = Users.find_by({'email': 'test@test'})
        self.assertEqual('test@test', user.email)


if __name__ == '__main__':
    unittest.main()
