from typing import Any, Tuple, Optional

import mysql.connector

from domain.models.transaction_model import TransactionModel
from infra.database_connection.mysql_connection import MySqlConnection


class DigitalAccountRepository:
    def __init__(self):
        self.conn = MySqlConnection().connect_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def get_digital_account(self, digital_account_id: int,
                            digital_account_agency: int):
        data = {
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency
        }
        query = "SELECT * " \
                "FROM digital_accounts " \
                "WHERE digital_account_id = %(digital_account_id)s " \
                "AND digital_account_agency = %(digital_account_agency)s;"

        self.cursor.execute(query, data)
        result = self.cursor.fetchone()
        return result

    def get_user_digital_account(self, user_id: int):
        data = {
            "user_id": user_id
        }
        query = "SELECT * " \
                "FROM digital_accounts " \
                "WHERE user_id = %(user_id)s"

        self.cursor.execute(query, data)
        result = self.cursor.fetchone()
        return result

    def insert_digital_account(self,
                               user_id: int,
                               digital_account_agency: int = 100,
                               total: float = 0.0) -> Tuple[int, int]:
        data = {
            "digital_account_agency": digital_account_agency,
            "user_id": user_id,
            "total": total
        }
        query = "INSERT INTO digital_accounts (digital_account_agency, user_id, total) " \
                "VALUES (%(digital_account_agency)s, %(user_id)s, %(total)s);"
        result = self.cursor.execute(query, data, multi=True)
        last_inserted_id = next(result).lastrowid
        self.conn.commit()
        return last_inserted_id, digital_account_agency

    def do_deposit(self, transaction_model: TransactionModel) -> bool:
        try:
            prev_values = self.select_total(digital_account_id=transaction_model.digital_account_id,
                                            digital_account_agency=transaction_model.digital_account_agency)
            prev_total = prev_values.get("total")

            new_total = prev_total + transaction_model.value
            result = self.update_digital_account_total(digital_account_id=transaction_model.digital_account_id,
                                                       digital_account_agency=transaction_model.digital_account_agency,
                                                       total=new_total)
            self.conn.commit()
            if result > 0:
                return True
            return False
        except mysql.connector.Error as error:
            self.conn.rollback()
            return False

    def do_withdraw(self, transaction_model: TransactionModel) -> bool:
        try:
            prev_values = self.select_total(digital_account_id=transaction_model.digital_account_id,
                                            digital_account_agency=transaction_model.digital_account_agency)
            prev_total = prev_values.get("total")
            prev_withdraw_daily_limit = prev_values.get("withdraw_daily_limit")

            new_total = prev_total - transaction_model.value
            new_withdraw_daily_limit = prev_withdraw_daily_limit - transaction_model.value

            result = self.update_digital_account_total(digital_account_id=transaction_model.digital_account_id,
                                                       digital_account_agency=transaction_model.digital_account_agency,
                                                       total=new_total,
                                                       withdraw_daily_limit=new_withdraw_daily_limit)
            self.conn.commit()
            if result > 0:
                return True
            return False
        except mysql.connector.Error as error:
            self.conn.rollback()
            return False

    def select_total(self,
                     digital_account_id: int,
                     digital_account_agency: int) -> dict:
        data = {
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency
        }
        query = "SELECT total, withdraw_daily_limit " \
                "FROM digital_accounts " \
                "WHERE digital_account_id = %(digital_account_id)s " \
                "AND digital_account_agency = %(digital_account_agency)s " \
                "FOR UPDATE OF digital_accounts;"
        self.cursor.execute(query, data)
        result = self.cursor.fetchone()
        return result

    def update_digital_account_total(self,
                                     digital_account_id: int,
                                     digital_account_agency: int,
                                     total: float,
                                     withdraw_daily_limit: Optional[float] = None):
        data = {
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency,
            "total": total
        }
        if withdraw_daily_limit is not None:
            set_clause = f"SET total = %(total)s, withdraw_daily_limit = %(withdraw_daily_limit)s"
            data["withdraw_daily_limit"] = withdraw_daily_limit
        else:
            set_clause = "SET total = %(total)s"

        update_query = "UPDATE digital_accounts " \
                       f"{set_clause} " \
                       "WHERE digital_account_id = %(digital_account_id)s " \
                       "AND digital_account_agency = %(digital_account_agency)s;"
        self.cursor.execute(update_query, data)
        return self.cursor.rowcount

    def change_account_active_status(self,
                                     digital_account_id: int,
                                     digital_account_agency: int,
                                     active_account: Optional[bool]) -> int:
        data = {
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency,
        }

        if active_account is not None:
            is_active = active_account
        else:
            is_active = 'NOT is_active'

        update_query = "UPDATE digital_accounts " \
                       f"SET is_active = {is_active} " \
                       "WHERE digital_account_id = %(digital_account_id)s " \
                       "AND digital_account_agency = %(digital_account_agency)s;"
        self.cursor.execute(update_query, data)
        result = self.cursor.rowcount
        self.conn.commit()
        return result

    def change_account_block_status(self,
                                    digital_account_id: int,
                                    digital_account_agency: int,
                                    block_account: Optional[bool] = None) -> int:
        data = {
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency,
        }

        if block_account is not None:
            is_blocked = block_account
        else:
            is_blocked = 'NOT is_blocked'

        update_query = "UPDATE digital_accounts " \
                       f"SET is_blocked = {is_blocked} " \
                       "WHERE digital_account_id = %(digital_account_id)s " \
                       "AND digital_account_agency = %(digital_account_agency)s;"
        self.cursor.execute(update_query, data)
        result = self.cursor.rowcount
        self.conn.commit()
        return result

    def delete_digital_account(self, digital_account_id: int, digital_account_agency: int) -> int:
        data = {
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency,
        }
        query = "DELETE FROM digital_accounts " \
                "WHERE digital_account_id = %(digital_account_id)s " \
                "AND digital_account_agency = %(digital_account_agency)s;"
        result = self.cursor.execute(query, data, multi=True)
        self.conn.commit()

        return next(result).rowcount
