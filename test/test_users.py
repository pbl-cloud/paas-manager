import unittest
from ..paas_manager.app.users import is_registered


class TestUsers(unittest.TestCase):
    def test_is_registered(self):
        self.assertTrue((is_registered('user1@example.com')))
        

if __name__ == '__main__':
    unittest.main()
