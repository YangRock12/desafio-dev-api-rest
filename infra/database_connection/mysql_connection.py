import mysql.connector

from cross_cutting.configs import DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_DATABASE
from domain.helpers.singleton_helper import SingletonMeta

CONFIG = {
    "host": DB_HOSTNAME,
    "user": DB_USERNAME,
    "password": DB_PASSWORD,
    "database": DB_DATABASE
}


class MySqlConnection(metaclass=SingletonMeta):
    @staticmethod
    def connect_db():
        conn = mysql.connector.connect(**CONFIG, autocommit=True)
        return conn
