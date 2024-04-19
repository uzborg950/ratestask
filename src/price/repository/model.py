from pydantic import BaseModel


class PriceRequestDAO(BaseModel):
    date_from: str
    date_to: str
    origin: str
    destination: str
    min_sample_size: int


class AvgPriceResponseDAO(BaseModel):
    day: str
    avg_price: float
    count: int
