import hashlib
from .database_connector import DatabaseConnector


def _hash_password(email, password):
    email = email.encode()
    password = password.encode()
    salt = hashlib.sha1(email).hexdigest().encode()
    hashed_password = hashlib.sha1(password + salt).hexdigest().encode()
    for i in range(100):
        hashed_password = hashlib.sha1(hashed_password).hexdigest().encode()
    return hashed_password.decode()

class Users(DatabaseConnector):
    table = 'users'

    @classmethod
    def authorize(cls, email, password):
        user = Users.find_by({'email': email})
        if user and user.hashed_password == _hash_password(email, password):
            return user
        return False

    def before_save(self):
        if hasattr(self, 'password'):
            self.hashed_password = _hash_password(self.email, self.password)
            del self.password
