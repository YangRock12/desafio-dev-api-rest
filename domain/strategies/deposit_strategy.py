from domain.models.transaction_model import TransactionModel
from domain.services.transaction_service import TransactionService
from domain.strategies.abstract_strategy import Strategy
from infra.repositories.digital_account_repository import DigitalAccountRepository


class DepositStrategy(Strategy):
    def __init__(self):
        self.transaction_service = TransactionService()
        self.digital_account_repository = DigitalAccountRepository()

    def do_algorithm(self, context: dict, transaction_model: TransactionModel) -> bool:
        result = self.digital_account_repository.do_deposit(transaction_model=transaction_model)
        return result
