from datetime import datetime

from domain.models.transaction_model import TransactionModel
from infra.database_connection.mysql_connection import MySqlConnection


class TransactionRepository:
    def __init__(self):
        self.conn = MySqlConnection().connect_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def get_statement_by_period(self,
                                start_date: str,
                                end_date: str,
                                digital_account_id: int,
                                digital_account_agency: int):
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "digital_account_id": digital_account_id,
            "digital_account_agency": digital_account_agency
        }

        query = "SELECT * " \
                "FROM financial_transactions " \
                "WHERE digital_account_id = %(digital_account_id)s " \
                "AND digital_account_agency = %(digital_account_agency)s " \
                "AND operation_date >= %(start_date)s " \
                "AND operation_date <= %(end_date)s"

        result = self.cursor.execute(query, data, multi=True)
        if result:
            return next(result).fetchall()
        return result

    def save_historic(self, transaction_model: TransactionModel) -> bool:
        data = {
            "digital_account_id": transaction_model.digital_account_id,
            "digital_account_agency": transaction_model.digital_account_agency,
            "transaction_type_id": transaction_model.transaction_type_id,
            "value": transaction_model.value,
            "operation_date": transaction_model.operation_date or datetime.now(),
        }

        query = "INSERT INTO financial_transactions (digital_account_id, digital_account_agency, " \
                "transaction_type_id, movement_value, operation_date) " \
                "VALUES (%(digital_account_id)s, %(digital_account_agency)s, " \
                "%(transaction_type_id)s, %(value)s, %(operation_date)s);"

        self.cursor.execute(query, data)
        self.conn.commit()
        return True

    def delete_digital_account_transactions(self, digital_account_id: int) -> int:
        data = {
            "digital_account_id": digital_account_id
        }
        query = "DELETE FROM financial_transactions " \
                "WHERE digital_account_id = %(digital_account_id)s;"
        result = self.cursor.execute(query, data)
        self.conn.commit()
        return next(result).rowcount
