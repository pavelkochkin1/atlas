from typing import Optional

from pydantic import BaseModel


# ----- SemanticBlock -----
class SemanticBlock(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
