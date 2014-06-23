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
    def register_user(cls, email, password):
        if cls.is_registered(email):
            return
        hashed_password = _hash_password(email, password)
        cls.cursor.execute('insert into ' + cls.table + ' (email, hashed_password) values (%s, %s)', (email, hashed_password))
        cls.connect.commit()

    @classmethod
    def authorize(cls, email, password):
        if cls.is_registered(email):
           id = cls.verify_password(email, password)
        return id if id else False

    @classmethod
    def is_registered(cls, email):
        try:
            cls.user_id(email)
            return True
        except:
            return False

    @classmethod
    def verify_password(cls, email, password):
        hashed_password = _hash_password(email, password)
        cls.cursor.execute('select id, hashed_password from ' + cls.table + ' where email = %s', (email,))
        rows = cls.cursor.fetchall()
        if len(rows) == 0:
            raise Exception('User not found')
        if rows[0][1] == hashed_password:
            return rows[0][0]
        else:
            return None

    def delete_user(self, email):
        if not self.is_registered(email):
            raise Exception('User not found')
        self.cursor.execute('delete from ' + self.table + ' where email = %s', (email,))
        self.connect.commit()

    @classmethod
    def user_id(cls, email):
        cls.cursor.execute('select id from ' + cls.table + ' where email = %s', (email,))
        rows = cls.cursor.fetchall()
        if len(rows) == 0:
            raise Exception('User not found')
        return rows[0][0]

