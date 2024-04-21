from src.port.repository.port_repository import PortRepository
from src.port.service.model import PortDTO
from test.database.db_test import database


def test_get_all_by_region_slug_for_top_most_region(database):
    port_repository = PortRepository(database)
    port_dtos = port_repository.get_all_by_region_slug('top_most_region')
    assert isinstance(port_dtos, list)
    port_codes = [port_dto.code for port_dto in port_dtos]
    expected_codes = set(['BOTP1', 'MIDP1', 'MIDP2', 'TOPP1'])
    difference = expected_codes ^ set(port_codes)
    assert not difference


def test_get_all_by_region_slug_for_middle_region(database):
    port_repository = PortRepository(database)
    port_dtos = port_repository.get_all_by_region_slug('middle_region')
    assert isinstance(port_dtos, list)
    port_codes = [port_dto.code for port_dto in port_dtos]
    expected_codes = set(['BOTP1', 'MIDP1', 'MIDP2'])
    difference = expected_codes ^ set(port_codes)
    assert not difference


def test_get_by_code(database):
    port_repository = PortRepository(database)
    port_dto = port_repository.get_by_code('EXTPP')
    assert isinstance(port_dto, PortDTO)
    assert port_dto.code == 'EXTPP'
    assert port_dto.parent_slug == 'external_region'
    assert port_dto.name == 'port at external region'