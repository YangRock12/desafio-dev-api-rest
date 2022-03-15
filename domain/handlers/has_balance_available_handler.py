from typing import Any

from domain.enums.transaction_validation_enum import TransactionValidationEnum
from domain.handlers.abstract_base_handlers import AbstractHandler
from domain.models.digital_account_model import DigitalAccountModel
from domain.models.transaction_model import TransactionModel


class HasBalanceAvailableHandler(AbstractHandler):
    def handle(self, context: Any) -> TransactionValidationEnum:
        digital_account = context.get("digital_account", DigitalAccountModel())
        transaction_model = context.get("transaction_model", TransactionModel())

        if digital_account.total < transaction_model.value:
            return TransactionValidationEnum.no_balance_available
        else:
            return super().handle(context=context)
