from src.region.repository.region_repository import RegionRepository


class RegionService:
    def __init__(self, region_respository: RegionRepository):
        self._region_respository = region_respository

    def get_by_slug(self, slug: str):
        return self._region_respository.get_by_slug(slug)
