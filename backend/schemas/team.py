from pydantic import BaseModel


# ----- Team -----
class Team(BaseModel):
    name: str
    id: str
