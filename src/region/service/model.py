from pydantic import BaseModel


class RegionDTO(BaseModel):
    slug: str
    name: str
    parent_slug: str