import unittest
from paas_manager.app.users import *


class TestUsers(unittest.TestCase):
    def test_is_registered(self):
        self.assertTrue((is_registered('user1@example.com')))

    def test_user(self):
        register_user('test@test', 'test')
        self.assertTrue(login_user('test@test', 'test'))
        delete_user('test@test')


if __name__ == '__main__':
    unittest.main()
