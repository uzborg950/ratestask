from datetime import datetime
from typing import List

from fastapi import APIRouter

import src.price.service.price_service as price_service
from src.exceptions.exception_handlers import RequestValidationException, InvalidDateRangeException
from src.price.controller.model import AvgPriceResponse
from src.price.controller.validation import validate_date
from src.price.service.model import PriceRequestDTO
from src.utils.constants import DATE_FORMAT

router = APIRouter(
    prefix="/price",
    tags=["price"],
    responses={404: {"description": "Not found"}},
)


@router.get("/avgPriceForRange", response_model=List[AvgPriceResponse])
async def get_avg_price_for_range(date_from: str, date_to: str, origin: str, destination: str, impute_with_null=True,
                                  min_sample_size=3) -> List[AvgPriceResponse]:
    """
    Get average price of a given date range for a route or groups of routes
    :param date_from: inclusive start date for calculating average price
    :param date_to: inclusive end date for calculating average price
    :param origin: port code or slug of origin
    :param destination: port code or slug of destination
    :param impute_with_null: impute days with invalid average price with null
    :param min_sample_size: sample size required before calculating average price for a given day
    :return:
    """
    # request validation
    if not validate_date(date_from):
        raise RequestValidationException(param_name="date_from", param_value=date_from,
                                         extra_message='Expected format is: YYYY-MM-DD')
    if not validate_date(date_to):
        raise RequestValidationException(param_name="date_to", param_value=date_to,
                                         extra_message='Expected format is: YYYY-MM-DD')

    date_from_parsed = datetime.strptime(date_from, DATE_FORMAT)
    date_to_parsed = datetime.strptime(date_to, DATE_FORMAT)

    if date_from_parsed > date_to_parsed:
        raise InvalidDateRangeException(date_from_param="date_from", date_from_value=date_from, date_to_param='date_to',
                                        date_to_value=date_to)

    price_request = PriceRequestDTO(date_from=date_from_parsed, date_to=date_to_parsed, origin=origin,
                                    destination=destination, impute_with_null=impute_with_null,
                                    min_sample_size=min_sample_size)
    return price_service.get_avg_price(price_request)
