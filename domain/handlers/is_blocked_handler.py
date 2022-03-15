from typing import Any

from domain.enums.transaction_validation_enum import TransactionValidationEnum
from domain.handlers.abstract_base_handlers import AbstractHandler
from domain.models.digital_account_model import DigitalAccountModel


class IsBlockedHandler(AbstractHandler):
    def handle(self, context: Any) -> TransactionValidationEnum:
        digital_account = context.get("digital_account", DigitalAccountModel())

        if digital_account.is_blocked:
            return TransactionValidationEnum.is_blocked
        else:
            return TransactionValidationEnum.is_not_blocked
