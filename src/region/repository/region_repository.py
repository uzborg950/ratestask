from typing import Optional

from src.region.service.model import RegionDTO


class RegionRepository:
    def __init__(self, conn):
        self.db = conn.cursor()

    def get_by_slug(self, slug: str) -> Optional[RegionDTO]:
        self.db.execute("""SELECT slug,name,parent_slug FROM regions WHERE slug=%(slug)s""", {'slug': slug})
        result = self.db.fetchone()
        return RegionDTO(slug=result[0], name=result[1], parent_slug=result[2]) if result else None
