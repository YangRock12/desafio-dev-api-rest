from abc import ABC, abstractmethod

from domain.models.transaction_model import TransactionModel


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def do_algorithm(self, context: dict, transaction_model: TransactionModel):
        pass
