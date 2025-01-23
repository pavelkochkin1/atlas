from typing import Optional

from pydantic import BaseModel


# ----- Field -----
class FieldCreate(BaseModel):
    name: str
    description: Optional[str] = None


class FieldRead(FieldCreate):
    id: str
