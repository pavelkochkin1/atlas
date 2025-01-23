from pydantic import BaseModel, EmailStr


# ----- Person -----
class Person(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
