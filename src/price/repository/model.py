from typing import List

from pydantic import BaseModel


class PriceRequestDAO(BaseModel):
    date_from: str
    date_to: str
    origins: List[str]
    destinations: List[str]
    min_sample_size: int


class AvgPriceResponseDAO(BaseModel):
    day: str
    avg_price: float
    count: int
