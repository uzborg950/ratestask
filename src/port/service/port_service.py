from typing import Optional, List

from src.port.service.model import PortDTO
import src.port.repository.port_repository as repo


def get_by_code(code: str) -> Optional[PortDTO]:
    return repo.get_by_code(code)


def get_all_by_region_slug(slug: str) -> List[PortDTO]:
    """
    Get all ports within a given region.
    This does a recursive search inside a region, digging into the sub-regions to fetch all ports
    :param slug: region slug
    :return: list of PortDTOs
    """
    return repo.get_all_by_region_slug(slug)