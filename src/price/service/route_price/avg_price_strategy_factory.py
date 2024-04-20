from abc import abstractmethod, ABC
from typing import List, Optional

import src.port.service.port_service as port_service
import src.price.repository.price_repository as repo
import src.region.service.region_service as region_service
from src.price.repository.model import PriceRequestDAO
from src.price.service.model import AvgPriceDTO, PriceRequestDTO
from src.utils.constants import DATE_FORMAT


def get_codes_in_region(region: str):
    port_dtos = port_service.get_all_by_region_slug(region)
    return [port_dto.code for port_dto in port_dtos]


# Strategy Pattern
class AvgPriceStrategy(ABC):
    @abstractmethod
    def process(self, price_request: PriceRequestDTO) -> List[AvgPriceDTO]:
        pass


class PortToRegionStrategy(AvgPriceStrategy):
    def process(self, price_request: PriceRequestDTO):
        dest_codes = get_codes_in_region(price_request.destination)
        return repo.get_avg_price(PriceRequestDAO(date_from=price_request.date_from.strftime(DATE_FORMAT),
                                                  date_to=price_request.date_to.strftime(DATE_FORMAT),
                                                  origins=[price_request.origin],
                                                  destinations=dest_codes,
                                                  min_sample_size=price_request.min_sample_size))


class RegionToPortStrategy(AvgPriceStrategy):
    def process(self, price_request: PriceRequestDTO):
        orig_codes = get_codes_in_region(price_request.origin)
        return repo.get_avg_price(PriceRequestDAO(date_from=price_request.date_from.strftime(DATE_FORMAT),
                                                  date_to=price_request.date_to.strftime(DATE_FORMAT),
                                                  origins=orig_codes,
                                                  destinations=[price_request.destination],
                                                  min_sample_size=price_request.min_sample_size))


class PortToPortStrategy(AvgPriceStrategy):
    def process(self, price_request: PriceRequestDTO):
        return repo.get_avg_price(PriceRequestDAO(date_from=price_request.date_from.strftime(DATE_FORMAT),
                                                  date_to=price_request.date_to.strftime(DATE_FORMAT),
                                                  origins=[price_request.origin],
                                                  destinations=[price_request.destination],
                                                  min_sample_size=price_request.min_sample_size))


class RegionToRegionStrategy(AvgPriceStrategy):
    def process(self, price_request: PriceRequestDTO):
        dest_codes = get_codes_in_region(price_request.destination)
        orig_codes = get_codes_in_region(price_request.origin)
        return repo.get_avg_price(PriceRequestDAO(date_from=price_request.date_from.strftime(DATE_FORMAT),
                                                  date_to=price_request.date_to.strftime(DATE_FORMAT),
                                                  origins=orig_codes,
                                                  destinations=dest_codes,
                                                  min_sample_size=price_request.min_sample_size))


# Factory pattern
class AvgPriceStrategyFactory:
    """
    Factory class that creates AvgPriceStrategy instances.
    Each strategy is a combination of port and region or port only or region only.
    """

    @staticmethod
    def create_strategy(origin: str, destination: str) -> Optional[AvgPriceStrategy]:
        is_origin_port = port_service.get_by_code(origin)
        is_origin_region = region_service.get_by_slug(origin)
        is_destination_port = port_service.get_by_code(destination)
        is_destination_region = region_service.get_by_slug(destination)

        if is_origin_port and is_destination_port:
            return PortToPortStrategy()
        elif is_origin_port and is_destination_region:
            return PortToRegionStrategy()
        elif is_origin_region and is_destination_port:
            return RegionToPortStrategy()
        elif is_origin_region and is_destination_region:
            return RegionToRegionStrategy()

        # default case is None for invalid data
