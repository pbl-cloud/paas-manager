import mysql.connector

from ... import config


class DatabaseConnector():
    connect = mysql.connector.connect(**config['mysql'])
    cursor = connect.cursor()
