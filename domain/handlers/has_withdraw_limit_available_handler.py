from typing import Any

from domain.enums.transaction_validation_enum import TransactionValidationEnum
from domain.handlers.abstract_base_handlers import AbstractHandler
from domain.models.digital_account_model import DigitalAccountModel
from domain.models.transaction_model import TransactionModel


class HasWithdrawLimitAvailable(AbstractHandler):
    def handle(self, context: Any) -> TransactionValidationEnum:
        digital_account = context.get("digital_account", DigitalAccountModel())
        transaction_model = context.get("transaction_model", TransactionModel())

        if digital_account.withdraw_daily_limit < transaction_model.value:
            return TransactionValidationEnum.no_withdraw_daily_limit_available
        else:
            return TransactionValidationEnum.withdraw_daily_limit_available
