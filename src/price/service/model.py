import typing
from datetime import datetime, date
from typing import Dict

from pydantic import BaseModel


class PriceRequestDTO(BaseModel):
    date_from: datetime
    date_to: datetime
    origin: str
    destination: str
    impute_with_null: bool
    min_sample_size: int


class AvgPriceDTO(BaseModel):
    average_price: float
    day: datetime
    count: int
