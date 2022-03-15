from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionModel(BaseModel):
    digital_account_id: int = 0
    digital_account_agency: int = 0
    transaction_type_id: int = 0
    value: float = 0.0
    operation_date: Optional[datetime] = datetime.now()
