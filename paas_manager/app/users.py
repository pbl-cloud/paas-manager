import hashlib
import mysql.connector
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
    def register_user(self, email, password):
        if self.is_registered(email):
            return
        hashed_password = _hash_password(email, password)
        self.cursor.execute('insert into users (email, hashed_password) values (%s, %s)', (email, hashed_password))
        self.connect.commit()

    def is_registered(self, email):
        try:
            self.user_id(email)
            return True
        except:
            return False

    def verify_password(self, email, password):
        hashed_password = _hash_password(email, password)
        self.cursor.execute('select hashed_password from users where email = %s', (email,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise Exception('User not found')
        return rows[0][0] == hashed_password

    def delete_user(self, email):
        if not self.is_registered(email):
            raise Exception('User not found')
        self.cursor.execute('delete from users where email = %s', (email,))
        self.connect.commit()

    def user_id(self, email):
        self.cursor.execute('select userid from users where email = %s', (email,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            raise Exception('User not found')
        return rows[0][0]
