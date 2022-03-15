from typing import Any

from domain.enums.transaction_validation_enum import TransactionValidationEnum
from domain.handlers.abstract_base_handlers import AbstractHandler
from domain.models.digital_account_model import DigitalAccountModel


class IsActiveHandler(AbstractHandler):
    def handle(self, context: Any) -> TransactionValidationEnum:
        digital_account = context.get("digital_account", DigitalAccountModel())

        if not digital_account.is_active:
            return TransactionValidationEnum.is_not_active
        else:
            return super().handle(context=context)
