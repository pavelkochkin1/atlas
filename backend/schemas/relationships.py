from pydantic import BaseModel


class AddFieldRequest(BaseModel):
    table_name: str
    field_id: str


class SourceOfRequest(BaseModel):
    source_name: str
    target_name: str


class BelongsToIndustryRequest(BaseModel):
    table_name: str
    industry_id: str


class MaintainedByRequest(BaseModel):
    table_name: str
    team_id: str


class HasResponsibleRequest(BaseModel):
    table_name: str
    person_email: str


class PartOfRequest(BaseModel):
    table_name: str
    block_id: str


class BelongsToTeamRequest(BaseModel):
    email: str
    team_id: str


class FieldReferencesRequest(BaseModel):
    field_id: str
    ref_field_id: str
