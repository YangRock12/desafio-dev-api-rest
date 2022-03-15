from typing import Any

from domain.models.transaction_model import TransactionModel
from domain.strategies.abstract_strategy import Strategy


class Context:
    def __init__(self, strategy: Strategy,
                 data: dict,
                 transaction_model: TransactionModel) -> None:
        self._strategy = strategy
        self._data = data
        self._transaction_model = transaction_model

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_transaction(self) -> Any:
        result = self._strategy.do_algorithm(context=self._data,
                                             transaction_model=self._transaction_model)
        return result
