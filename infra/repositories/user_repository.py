from typing import Optional

from domain.models.user_model import UserModel
from infra.database_connection.mysql_connection import MySqlConnection


class UserRepository:
    def __init__(self):
        self.conn = MySqlConnection().connect_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def get_user(self, user_id: int) -> dict:
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM users WHERE user_id = %(user_id)s"

        self.cursor.execute(query, data)
        return self.cursor.fetchone()

    def insert_user(self, user: UserModel) -> Optional[int]:
        query = "INSERT INTO users (document, name) " \
                "VALUES (%(document)s, %(name)s);"
        data = {
            "name": user.name,
            "document": user.document,
        }

        result = self.cursor.execute(query, data, multi=True)
        last_inserted_id = next(result).lastrowid
        self.conn.commit()

        return last_inserted_id

    def delete_user(self, user_id: int) -> Optional[int]:
        query = "DELETE FROM users " \
                "WHERE user_id = %(user_id)s;"
        data = {
            "user_id": user_id
        }

        result = self.cursor.execute(query, data, multi=True)
        self.conn.commit()

        return next(result).rowcount
