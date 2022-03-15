from enum import IntEnum


class TransactionTypeEnum(IntEnum):
    transaction_unknown = 0
    withdraw = 1
    deposit = 2
