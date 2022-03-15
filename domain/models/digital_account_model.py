from typing import Optional

from pydantic import BaseModel


class DigitalAccountModel(BaseModel):
    digital_account_id: Optional[int] = 0
    digital_account_agency: int = 0
    user_id: int = 0
    total: float = 0.0
    withdraw_daily_limit: float = 0.0
    is_active: Optional[bool] = False
    is_blocked: Optional[bool] = True
