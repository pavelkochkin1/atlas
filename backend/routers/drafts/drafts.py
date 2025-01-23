from collections import defaultdict
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from schemas.draft import TableDraft

drafts_router = APIRouter()


drafts: Dict[EmailStr, List[TableDraft]] = defaultdict(list)


@drafts_router.post("/", status_code=200)
async def create_draft(table_draft: TableDraft):
    drafts[table_draft.responsible_person].append(table_draft)
    return {"message": "Draft created"}


@drafts_router.get("/", response_model=List[TableDraft])
async def get_draft(email: EmailStr):
    return drafts.get(email, [])


@drafts_router.delete("/", status_code=200)
async def delete_draft(email: EmailStr, table_name: str):
    print("email: ", email, "table_name: ", table_name)
    if email not in drafts:
        raise HTTPException(status_code=404, detail="Draft not found")
    for draft in drafts[email]:
        if draft.name == table_name:
            drafts[email].remove(draft)
            break
    return {"message": "Draft deleted"}
