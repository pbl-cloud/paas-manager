import unittest
from paas_manager.app import users


class TestUsers(unittest.TestCase):
    def setUp(self):
        users.register_user('test@test', 'test')

    def tearDown(self):
        users.delete_user('test@test')

    def test_is_registered(self):
        self.assertTrue((users.is_registered('test@test')))

    def test_verify_success(self):
        self.assertTrue(users.verify_password('test@test', 'test'))

    def test_verify_failed(self):
        self.assertFalse(users.verify_password('test@test', 'pass'))


if __name__ == '__main__':
    unittest.main()
