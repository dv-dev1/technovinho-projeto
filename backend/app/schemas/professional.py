from pydantic import BaseModel, Field


class ProfessionalCreate(BaseModel):
    user_id: int
    specialty: str | None = Field(default=None, max_length=100)
    active: bool = True


class ProfessionalUpdate(BaseModel):
    specialty: str | None = Field(default=None, max_length=100)
    active: bool | None = None


class ProfessionalOut(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    specialty: str | None
    active: bool

    model_config = {"from_attributes": True}
