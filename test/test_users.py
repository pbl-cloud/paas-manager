import unittest
from paas_manager.app.users import Users


class TestUsers(unittest.TestCase):
    users = Users()
    users.table = 'test_users'

    def setUp(self):
        self.users.register_user('test@test', 'test')

    def tearDown(self):
        self.users.delete_user('test@test')

    def test_is_registered(self):
        self.assertTrue((self.users.is_registered('test@test')))

    def test_verify_success(self):
        self.assertEqual(self.users.verify_password('test@test', 'test'), self.users.user_id('test@test'))

    def test_verify_failed(self):
        self.assertEqual(self.users.verify_password('test@test', 'pass'), None)

    def test_user_id(self):
        id = self.users.user_id('test@test')

if __name__ == '__main__':
    unittest.main()
