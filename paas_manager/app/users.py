import hashlib
import mysql.connector


def mysql_execute(query):
    rows = None
    try:
        connect = mysql.connector.connect(user='app', password=None, host='192.168.122.9', database='paas',
                                          charset='utf8')
        cursor = connect.cursor()
        cursor.execute(query, ())
        if query.startswith('select'):
            rows = cursor.fetchall()
        else:
            connect.commit()
        cursor.close()
        connect.close()
        return rows
    except Exception as e:
        print(e)


def hash_password(email, password):
    if is_registered(email):
        return
    salt = hashlib.sha1(email)
    hashed_password = hashlib.sha1(password + salt)
    for i in range(100):
        hashed_password = hashlib.sha1(hashed_password)
    return hashed_password


def register_user(email, password):
    hashed_password = hash_password(email, password)
    mysql_execute('insert into users (email, hashed_password) values (' + email + ', ' + hashed_password)


def is_registered(email):
    rows = mysql_execute('select * from users where email = \'' + email + '\'')
    return len(rows) > 0


def login_user(email, password):
    if is_registered(email):
        raise Exception('User not found')
    hashed_password = hash_password(email, password)
    rows = mysql_execute('select hashed_password from users where email = \'' + email + '\'')
    return rows[0] == hashed_password


