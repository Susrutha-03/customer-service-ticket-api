
from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator, ConfigDict


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    customer_name: str = Field(min_length=2, max_length=100)

    priority: Literal["Low", "Medium", "High", "Critical"] = "Medium"

    @field_validator("title", "description", "customer_name", mode="before")
    @classmethod
    def clean_text(cls, value):
        if not isinstance(value, str):
            return value

        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty")

        return value


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    customer_name: str
    priority: str
    status: str
    assigned_to: Optional[str] = None
    sla_due_at: Optional[datetime] = None
