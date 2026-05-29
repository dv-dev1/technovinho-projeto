from pydantic import BaseModel, EmailStr, Field


class ProfessionalCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
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
