from src.database.db import conn
from src.port.repository.port_repository import PortRepository
from src.port.service.port_service import PortService
from src.price.repository.price_repository import PriceRepository
from src.price.service.price_service import PriceService
from src.region.repository.region_repository import RegionRepository
from src.region.service.region_service import RegionService

# dependency initialization

# region
region_repository = RegionRepository(conn)
region_service = RegionService(region_repository)

# port
port_repository = PortRepository(conn)
port_service = PortService(port_repository)

# price
price_repository = PriceRepository(conn)
price_service = PriceService(price_repository, port_service, region_service)
