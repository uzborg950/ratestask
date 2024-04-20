from pydantic import BaseModel


class PortDTO(BaseModel):
    code: str
    name: str
    parent_slug: str