from typing import Optional

from pydantic import BaseModel


# ----- Table -----
class Table(BaseModel):
    name: str
    description: Optional[str] = None
