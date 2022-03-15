from datetime import datetime

from domain.enums.transaction_validation_enum import TransactionValidationEnum
from domain.handlers.has_balance_available_handler import HasBalanceAvailableHandler
from domain.handlers.has_withdraw_limit_available_handler import HasWithdrawLimitAvailable
from domain.handlers.is_active_handler import IsActiveHandler
from domain.handlers.is_blocked_handler import IsBlockedHandler
from domain.models.transaction_model import TransactionModel
from infra.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self):
        self.is_active = IsActiveHandler()
        self.is_blocked = IsBlockedHandler()
        self.has_balance_available = HasBalanceAvailableHandler()
        self.has_withdraw_limit_available = HasWithdrawLimitAvailable()

        self.is_active.set_next(self.is_blocked)
        self.has_balance_available.set_next(self.has_withdraw_limit_available)

        self.transaction_repository = TransactionRepository()

    def basic_validate_transaction(self, context: dict) -> TransactionValidationEnum:
        result = self.is_active.handle(context=context)
        return result

    def validate_withdraw(self, context: dict) -> TransactionValidationEnum:
        result = self.has_balance_available.handle(context=context)
        return result

    def get_statement_by_period(self,
                                start_date: datetime,
                                end_date: datetime,
                                digital_account_id: int,
                                digital_account_agency: int):
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        return self.transaction_repository.get_statement_by_period(start_date=start_date,
                                                                   end_date=end_date,
                                                                   digital_account_id=digital_account_id,
                                                                   digital_account_agency=digital_account_agency)

    def save_historic(self, transaction_model: TransactionModel) -> bool:
        return self.transaction_repository.save_historic(transaction_model=transaction_model)

    def delete_digital_account_transactions(self, digital_account_id: int) -> int:
        return self.transaction_repository.delete_digital_account_transactions(digital_account_id=digital_account_id)
