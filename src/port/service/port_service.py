from typing import Optional, List

from src.port.repository.port_repository import PortRepository
from src.port.service.model import PortDTO


class PortService:
    def __init__(self, port_repository: PortRepository):
        self._port_repository = port_repository

    def get_by_code(self, code: str) -> Optional[PortDTO]:
        return self._port_repository.get_by_code(code)

    def get_all_by_region_slug(self, slug: str) -> List[PortDTO]:
        """
        Get all ports within a given region.
        This does a recursive search inside a region, digging into the sub-regions to fetch all ports
        :param slug: region slug
        :return: list of PortDTOs
        """
        return self._port_repository.get_all_by_region_slug(slug)
