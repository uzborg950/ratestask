from typing import Optional

from pydantic import BaseModel


class AvgPriceResponse(BaseModel):
    day: str
    average_price: Optional[float]