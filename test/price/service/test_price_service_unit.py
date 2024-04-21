import datetime
from typing import List

import pytest

from src.exceptions.exception_handlers import InvalidRouteException
from src.port.repository.port_repository import PortRepository
from src.port.service.port_service import PortService
from src.price.repository.price_repository import PriceRepository
from src.price.service.model import AvgPriceDTO, PriceRequestDTO
from src.price.service.price_service import PriceService
from src.price.service.route_price.avg_price_strategy_factory import AvgPriceStrategy
from src.region.repository.region_repository import RegionRepository
from src.region.service.region_service import RegionService


class MockPriceRepository(PriceRepository):
    pass


class MockRegionRepository(RegionRepository):
    pass


class MockRegionService(RegionService):
    pass


class MockPortRepository(PortRepository):
    pass


class MockPortService(PortService):
    pass


class MockConnection():
    def cursor(self):
        pass


def test_get_avg_price_given_invalid_origin(mocker):
    price_service = PriceService(price_repository=MockPriceRepository(conn=MockConnection()),
                                 region_service=MockRegionService(MockRegionRepository(conn=MockConnection())),
                                 port_service=MockPortService(MockPortRepository(conn=MockConnection())), )

    mocker.patch('src.price.service.price_service.AvgPriceStrategyFactory.create_strategy', return_value=None)

    with pytest.raises(InvalidRouteException):
        price_service.get_avg_price(
            PriceRequestDTO(date_from=datetime.datetime(2016, 1, 1, 0, 0), date_to=datetime.datetime(2016, 1, 2, 0, 0)
                            , origin='ABCDE', destination='HIJKLM', impute_with_null=True, min_sample_size=3))


def test_get_avg_price_containing_two_null_averages(mocker):
    class MockAvgPriceStrategy(AvgPriceStrategy):
        def process(self) -> List[AvgPriceDTO]:
            return [AvgPriceDTO(average_price=10.0, day=datetime.datetime(2016, 1, 1, 0, 0), count=5),
                    AvgPriceDTO(average_price=10.0, day=datetime.datetime(2016, 1, 4, 0, 0), count=5)]

    price_request_dto = PriceRequestDTO(date_from=datetime.datetime(2016, 1, 1, 0, 0),
                                        date_to=datetime.datetime(2016, 1, 4, 0, 0)
                                        , origin='ABCDE', destination='HIJKLM', impute_with_null=True,
                                        min_sample_size=3)
    mocker.patch('src.price.service.price_service.AvgPriceStrategyFactory.create_strategy',
                 return_value=MockAvgPriceStrategy(price_request=price_request_dto))
    price_service = PriceService(price_repository=MockPriceRepository(conn=MockConnection()),
                                 region_service=MockRegionService(MockRegionRepository(conn=MockConnection())),
                                 port_service=MockPortService(MockPortRepository(conn=MockConnection())), )

    avg_price_responses = price_service.get_avg_price(price_request_dto)
    assert avg_price_responses[0].average_price == 10.0
    assert avg_price_responses[0].day == '2016-01-01'

    assert avg_price_responses[1].average_price == None
    assert avg_price_responses[1].day == '2016-01-02'

    assert avg_price_responses[2].average_price == None
    assert avg_price_responses[2].day == '2016-01-03'

    assert avg_price_responses[3].average_price == 10.0
    assert avg_price_responses[3].day == '2016-01-04'

def test_get_avg_price_given_impute_with_null_false(mocker):
    class MockAvgPriceStrategy(AvgPriceStrategy):
        def process(self) -> List[AvgPriceDTO]:
            return [AvgPriceDTO(average_price=10.0, day=datetime.datetime(2016, 1, 1, 0, 0), count=5),
                    AvgPriceDTO(average_price=10.0, day=datetime.datetime(2016, 1, 4, 0, 0), count=5)]

    price_request_dto = PriceRequestDTO(date_from=datetime.datetime(2016, 1, 1, 0, 0),
                                        date_to=datetime.datetime(2016, 1, 4, 0, 0)
                                        , origin='ABCDE', destination='HIJKLM', impute_with_null=False,
                                        min_sample_size=3)
    mocker.patch('src.price.service.price_service.AvgPriceStrategyFactory.create_strategy',
                 return_value=MockAvgPriceStrategy(price_request=price_request_dto))
    price_service = PriceService(price_repository=MockPriceRepository(conn=MockConnection()),
                                 region_service=MockRegionService(MockRegionRepository(conn=MockConnection())),
                                 port_service=MockPortService(MockPortRepository(conn=MockConnection())), )

    avg_price_responses = price_service.get_avg_price(price_request_dto)
    assert avg_price_responses[0].average_price == 10.0
    assert avg_price_responses[0].day == '2016-01-01'
    assert avg_price_responses[1].average_price == 10.0
    assert avg_price_responses[1].day == '2016-01-04'