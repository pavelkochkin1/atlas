from typing import List

from pydantic import BaseModel, EmailStr


class FieldBase(BaseModel):
    name: str
    description: str


class TableDraft(BaseModel):
    name: str
    industry: str | None
    description: str
    team: str | None
    responsible_person: EmailStr
    sources_tables: List[str] | None
    fields: List[FieldBase]
