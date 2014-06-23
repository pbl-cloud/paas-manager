import mysql.connector


class DatabaseConnector():
    connect = mysql.connector.connect(user='app', password=None, host='192.168.122.9', database='paas',
                                      charset='utf8')
    cursor = connect.cursor()
