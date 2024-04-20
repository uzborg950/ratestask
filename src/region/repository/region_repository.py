from typing import Optional

from src.database.db import conn
from src.region.service.model import RegionDTO

db = conn.cursor()


def get_by_slug(slug: str) -> Optional[RegionDTO]:
    db.execute("""SELECT slug,name,parent_slug FROM regions WHERE slug=%(slug)s""", {'slug': slug})
    result = db.fetchone()
    return RegionDTO(slug=result[0], name=result[1], parent_slug=result[2]) if result else None
