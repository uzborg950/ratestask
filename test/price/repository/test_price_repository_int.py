from src.price.repository.model import PriceRequestDAO
from src.price.repository.price_repository import PriceRepository
from src.utils.constants import DATE_FORMAT
from test.database.db_test import database


def test_get_avg_price_for_port_to_ports(database):
    price_repository = PriceRepository(database)
    avg_price_dtos = price_repository.get_avg_price(
        PriceRequestDAO(date_from='2016-01-01', date_to='2016-01-06', origins=['EXTPP'],
                        destinations=['BOTP1', 'MIDP1', 'MIDP2', 'TOPP1'], min_sample_size=3))
    assert isinstance(avg_price_dtos, list)
    assert len(avg_price_dtos) == 4
    assert avg_price_dtos[0].average_price == 14.4
    assert avg_price_dtos[0].day.strftime(DATE_FORMAT) == '2016-01-01'
    assert avg_price_dtos[0].count == 5  # 5 data points averages

    assert avg_price_dtos[1].average_price == 12.0
    assert avg_price_dtos[1].day.strftime(DATE_FORMAT) == '2016-01-02'
    assert avg_price_dtos[1].count == 3

    assert avg_price_dtos[2].average_price == 25.0
    assert avg_price_dtos[2].day.strftime(DATE_FORMAT) == '2016-01-04'  # 2016-01-03 is skipped due to < 3 data points
    assert avg_price_dtos[2].count == 3

    assert avg_price_dtos[3].average_price == 12.0
    assert avg_price_dtos[3].day.strftime(DATE_FORMAT) == '2016-01-06'
    assert avg_price_dtos[3].count == 3
