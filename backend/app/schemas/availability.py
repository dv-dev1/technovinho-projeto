from datetime import time

from pydantic import BaseModel, Field, model_validator


class AvailabilityCreate(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def end_after_start(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time deve ser maior que start_time")
        return self


class AvailabilityOut(BaseModel):
    id: int
    professional_id: int
    day_of_week: int
    start_time: time
    end_time: time

    model_config = {"from_attributes": True}
