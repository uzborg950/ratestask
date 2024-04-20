import datetime as dt
from typing import List

from src.exceptions.exception_handlers import InvalidRouteException
from src.price.controller.model import AvgPriceResponse
from src.price.repository.model import PriceRequestDAO
from src.price.service.model import PriceRequestDTO, AvgPriceDTO
from src.price.service.route_price.avg_price_strategy_factory import AvgPriceStrategyFactory
from src.utils.constants import DATE_FORMAT


def get_avg_price(price_request: PriceRequestDTO) -> List[AvgPriceResponse]:
    """
    Get average price of a given price request
    :param price_request: parameters for finding average price between ports or regions
    :return: list of average price responses
    """
    avg_price_strategy = AvgPriceStrategyFactory.create_strategy(origin=price_request.origin,
                                                                 destination=price_request.destination)

    if not avg_price_strategy:
        raise InvalidRouteException(origin=price_request.origin, destination=price_request.destination)
    avg_price_dtos = avg_price_strategy.process(price_request)

    if not price_request.impute_with_null:
        return [AvgPriceResponse(day=avg_price_dto.day.strftime(DATE_FORMAT), average_price=avg_price_dto.average_price)
                for avg_price_dto in avg_price_dtos]

    # go through each day and impute values if not exists
    start_date = price_request.date_from
    avg_price_dtos_index = 0
    avg_price_responses: List[AvgPriceResponse] = []

    while start_date <= price_request.date_to:
        if date_is_not_equal_at_index(avg_price_dtos, avg_price_dtos_index, start_date):
            # impute null average price for date
            avg_price_responses.append(
                AvgPriceResponse(day=start_date.strftime(DATE_FORMAT), average_price=None))
        else:
            # add valid average for date
            avg_price_responses.append(
                AvgPriceResponse(day=start_date.strftime(DATE_FORMAT),
                                 average_price=avg_price_dtos[avg_price_dtos_index].average_price))
            avg_price_dtos_index += 1
        start_date += dt.timedelta(days=1)
    return avg_price_responses


def date_is_not_equal_at_index(avg_price_dtos: List[AvgPriceDTO], avg_price_dtos_index: int, date: dt.datetime):
    return avg_price_dtos_index == len(avg_price_dtos) or avg_price_dtos[avg_price_dtos_index].day != date
