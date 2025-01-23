from typing import List

import requests
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


def post_draft(table: TableDraft):
    url = "http://atlas_backend:8073/api/drafts/"
    response: List[TableDraft] = requests.get(url, params={"email": table.responsible_person})
    drafts = response.json()
    all_tables_in_drafts = [draft["name"] for draft in drafts]

    if table.name in all_tables_in_drafts:
        return {"message": "Draft already exists"}

    url = "http://atlas_backend:8073/api/drafts/"
    requests.post(url, json=table.model_dump())

    if response.status_code != 200:
        return {"message": "Error creating draft"}
