import datetime

from pydantic import BaseModel


class PriceModel(BaseModel):
    origin_port: str
    destination_port: str
    day: datetime.date
    price: float
