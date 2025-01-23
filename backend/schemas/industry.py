from pydantic import BaseModel


# ----- Industry -----
class Industry(BaseModel):
    name: str
    id: str
