from enum import Enum


class TransactionValidationEnum(str, Enum):
    is_not_active = "is_not_active"
    is_blocked = "is_blocked"
    is_not_blocked = "is_not_blocked"
    no_balance_available = "no_balance_available"
    balance_available = "balance_available"
    no_withdraw_daily_limit_available = "no_withdraw_daily_limit_available"
    withdraw_daily_limit_available = "withdraw_daily_limit_available"
    authorized = "authorized"
    unknown_transaction = "transaction not recognized or missing information"
