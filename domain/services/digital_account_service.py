from datetime import timedelta
from typing import Optional

from domain.enums.transaction_type_enum import TransactionTypeEnum
from domain.enums.transaction_validation_enum import TransactionValidationEnum
from domain.helpers.date_helper import convert_str_to_date, generate_datetime
from domain.helpers.strategy_context_helper import Context
from domain.models.digital_account_model import DigitalAccountModel
from domain.models.transaction_model import TransactionModel
from domain.services.transaction_service import TransactionService
from domain.strategies.deposit_strategy import DepositStrategy
from domain.strategies.withdraw_strategy import WithdrawStrategy
from infra.repositories.digital_account_repository import DigitalAccountRepository


class DigitalAccountService:
    def __init__(self):
        self.digital_account_repository = DigitalAccountRepository()
        self.transaction_service = TransactionService()

    def get_user_digital_account(self, user_id: int) -> DigitalAccountModel or None:
        result = self.digital_account_repository.get_user_digital_account(user_id=user_id)
        if result:
            return DigitalAccountModel(**result).dict(exclude={"user_id"})
        return {}

    def get_statement_by_period(self,
                                digital_account_id: int,
                                digital_account_agency: int,
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None):
        if start_date:
            start_date = convert_str_to_date(date_as_string=start_date)
        else:
            start_date = generate_datetime(min_or_max_datetime="min")

        if end_date:
            temp_date = convert_str_to_date(date_as_string=end_date)
            end_date = temp_date + timedelta(hours=23, minutes=59, seconds=59)
        else:
            end_date = generate_datetime(min_or_max_datetime="max")

        result = self.transaction_service.get_statement_by_period(start_date=start_date,
                                                                  end_date=end_date,
                                                                  digital_account_id=digital_account_id,
                                                                  digital_account_agency=digital_account_agency)
        return result

    def get_digital_account(self,
                            digital_account_id: int,
                            digital_account_agency: int) -> DigitalAccountModel or dict:
        result = self.digital_account_repository.get_digital_account(digital_account_id=digital_account_id,
                                                                     digital_account_agency=digital_account_agency)
        if result:
            return DigitalAccountModel(**result)
        return {}

    def insert_digital_account(self, user_id: int):
        return self.digital_account_repository.insert_digital_account(user_id=user_id)

    def do_transaction(self, transaction_model: TransactionModel) -> dict:
        data = {
            "digital_account": self.get_digital_account(
                digital_account_id=transaction_model.digital_account_id,
                digital_account_agency=transaction_model.digital_account_agency),
            "transaction_model": transaction_model
        }

        result = False
        transaction = "unknown"
        if transaction_model.transaction_type_id == TransactionTypeEnum.withdraw:
            transaction = "withdraw"
            context = Context(strategy=WithdrawStrategy(),
                              data=data,
                              transaction_model=transaction_model)
        elif transaction_model.transaction_type_id == TransactionTypeEnum.deposit:
            transaction = "deposit"
            context = Context(strategy=DepositStrategy(),
                              data=data,
                              transaction_model=transaction_model)

        if transaction != "unknown":
            basic_valid_transaction = self.transaction_service.basic_validate_transaction(context=data)

            if basic_valid_transaction == TransactionValidationEnum.is_not_blocked:
                result = context.do_transaction()
                if result:
                    self.transaction_service.save_historic(transaction_model=transaction_model)

        return {
            "result": result,
            "transaction": transaction
        }

    def change_account_active_status(self,
                                     digital_account_id: int,
                                     digital_account_agency: int,
                                     active_account: Optional[bool] = None) -> int:
        return self.digital_account_repository.change_account_active_status(
            digital_account_id=digital_account_id,
            digital_account_agency=digital_account_agency,
            active_account=active_account)

    def change_account_block_status(self,
                                    digital_account_id: int,
                                    digital_account_agency: int,
                                    block_account: Optional[bool] = None) -> int:
        return self.digital_account_repository.change_account_block_status(
            digital_account_id=digital_account_id,
            digital_account_agency=digital_account_agency,
            block_account=block_account)

    def delete_digital_account(self,
                               digital_account_id: int,
                               digital_account_agency: int) -> int:
        return self.digital_account_repository.delete_digital_account(digital_account_id=digital_account_id,
                                                                      digital_account_agency=digital_account_agency)
