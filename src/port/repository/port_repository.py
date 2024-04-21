from typing import Optional, List

from src.port.service.model import PortDTO


class PortRepository:
    def __init__(self, conn):
        self._db = conn.cursor()

    def get_by_code(self, code: str) -> Optional[PortDTO]:
        self._db.execute("""SELECT p.code,p."name",p.parent_slug FROM ports p WHERE p.code = %(code)s """,
                         {"code": code})
        row = self._db.fetchone()
        return PortDTO(code=row[0], name=row[1], parent_slug=row[2]) if row else None

    def get_all_by_region_slug(self, region_slug: str) -> List[PortDTO]:
        """
        Gets all ports by region slug. This is a recursive search.
        results are fetched in depth first order. For debugging you can use the ordercol to track the order of recursion by slug.
        :param region_slug: slug to search for.
        :return: list of PortDTO
        """
        # The ordercol is good to have to track the recursion for debugging
        self._db.execute("""WITH RECURSIVE all_ports_in_region AS (
        SELECT r.slug, r.parent_slug, p.code port_code, p.name port_name, p.parent_slug port_parent_slug
        FROM regions r
        LEFT JOIN ports p ON r.slug = p.parent_slug
        WHERE r.slug = %(region_slug)s 
        UNION
        SELECT child_r.slug, child_r.parent_slug, p.code port_code, p.name port_name, p.parent_slug port_parent_slug
        FROM regions child_r
        JOIN all_ports_in_region parent_r ON parent_r.slug = child_r.parent_slug
        LEFT JOIN ports p ON child_r.slug = p.parent_slug
    ) SEARCH DEPTH FIRST BY slug SET ordercol
    SELECT * FROM all_ports_in_region where port_code is not null order by ordercol""", {"region_slug": region_slug})
        rows = self._db.fetchall()
        return [PortDTO(code=row[2], name=row[3], parent_slug=row[4]) for row in rows] if rows else []
