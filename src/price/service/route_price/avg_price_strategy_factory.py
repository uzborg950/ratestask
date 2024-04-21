from abc import abstractmethod, ABC
from typing import List, Optional

from src.port.service.port_service import PortService
from src.price.repository.model import PriceRequestDAO
from src.price.repository.price_repository import PriceRepository
from src.price.service.model import AvgPriceDTO, PriceRequestDTO
from src.region.service.region_service import RegionService
from src.utils.constants import DATE_FORMAT


def get_codes_in_region(region: str, port_service: PortService) -> List[str]:
    port_dtos = port_service.get_all_by_region_slug(region)
    return [port_dto.code for port_dto in port_dtos]


# Strategy Pattern
class AvgPriceStrategy(ABC):
    def __init__(self, price_request: PriceRequestDTO):
        self._price_request = price_request

    @abstractmethod
    def process(self) -> List[AvgPriceDTO]:
        pass


class PortToRegionStrategy(AvgPriceStrategy):
    def __init__(self, price_repository: PriceRepository, port_service: PortService,
                 price_request: PriceRequestDTO) -> None:
        super().__init__(price_request)
        self._price_repository = price_repository
        self._port_service = port_service

    def process(self):
        dest_codes = get_codes_in_region(self._price_request.destination, self._port_service)
        return self._price_repository.get_avg_price(
            PriceRequestDAO(date_from=self._price_request.date_from.strftime(DATE_FORMAT),
                            date_to=self._price_request.date_to.strftime(DATE_FORMAT),
                            origins=[self._price_request.origin],
                            destinations=dest_codes,
                            min_sample_size=self._price_request.min_sample_size))


class RegionToPortStrategy(AvgPriceStrategy):
    def __init__(self, price_repository: PriceRepository, port_service: PortService,
                 price_request: PriceRequestDTO) -> None:
        super().__init__(price_request)
        self._price_repository = price_repository
        self._port_service = port_service

    def process(self):
        orig_codes = get_codes_in_region(self._price_request.origin, self._port_service)
        return self._price_repository.get_avg_price(
            PriceRequestDAO(date_from=self._price_request.date_from.strftime(DATE_FORMAT),
                            date_to=self._price_request.date_to.strftime(DATE_FORMAT),
                            origins=orig_codes,
                            destinations=[self._price_request.destination],
                            min_sample_size=self._price_request.min_sample_size))


class PortToPortStrategy(AvgPriceStrategy):
    def __init__(self, price_repository: PriceRepository, price_request: PriceRequestDTO) -> None:
        super().__init__(price_request)
        self._price_repository = price_repository
        self._price_request = price_request

    def process(self):
        return self._price_repository.get_avg_price(
            PriceRequestDAO(date_from=self._price_request.date_from.strftime(DATE_FORMAT),
                            date_to=self._price_request.date_to.strftime(DATE_FORMAT),
                            origins=[self._price_request.origin],
                            destinations=[self._price_request.destination],
                            min_sample_size=self._price_request.min_sample_size))


class RegionToRegionStrategy(AvgPriceStrategy):
    def __init__(self, price_repository: PriceRepository, port_service: PortService,
                 price_request: PriceRequestDTO) -> None:
        super().__init__(price_request)
        self._price_repository = price_repository
        self._port_service = port_service

    def process(self):
        dest_codes = get_codes_in_region(self._price_request.destination, self._port_service)
        orig_codes = get_codes_in_region(self._price_request.origin, self._port_service)
        return self._price_repository.get_avg_price(
            PriceRequestDAO(date_from=self._price_request.date_from.strftime(DATE_FORMAT),
                            date_to=self._price_request.date_to.strftime(DATE_FORMAT),
                            origins=orig_codes,
                            destinations=dest_codes,
                            min_sample_size=self._price_request.min_sample_size))


# Factory pattern
class AvgPriceStrategyFactory:
    """
    Factory class that creates AvgPriceStrategy instances.
    Each strategy is a combination of port and region or port only or region only.
    """

    def __init__(self, port_service: PortService, region_service: RegionService,
                 price_repository: PriceRepository) -> None:
        self._port_service = port_service
        self._region_service = region_service
        self._price_repository = price_repository

    def create_strategy(self, price_request: PriceRequestDTO) -> Optional[AvgPriceStrategy]:
        is_origin_port = self._port_service.get_by_code(price_request.origin)
        is_origin_region = self._region_service.get_by_slug(price_request.origin)
        is_destination_port = self._port_service.get_by_code(price_request.destination)
        is_destination_region = self._region_service.get_by_slug(price_request.destination)

        if is_origin_port and is_destination_port:
            return PortToPortStrategy(self._price_repository, price_request)
        elif is_origin_port and is_destination_region:
            return PortToRegionStrategy(self._price_repository, self._port_service, price_request)
        elif is_origin_region and is_destination_port:
            return RegionToPortStrategy(self._price_repository, self._port_service, price_request)
        elif is_origin_region and is_destination_region:
            return RegionToRegionStrategy(self._price_repository, self._port_service, price_request)

        # default case is None for invalid data
