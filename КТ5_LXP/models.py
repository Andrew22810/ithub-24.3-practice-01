from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    """Модель пользователя Petstore API."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )

    id: int = Field(gt=0)
    username: str = Field(min_length=1)
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    email: str | None = None
    password: str | None = None
    phone: str | None = None
    user_status: int = Field(default=1, alias="userStatus", ge=0)


class Order(BaseModel):
    """Модель заказа Petstore API."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore"
    )

    id: int = Field(gt=0)
    pet_id: int = Field(alias="petId", gt=0)
    quantity: int = Field(gt=0)
    ship_date: datetime | None = Field(default=None, alias="shipDate")
    status: Literal["placed", "approved", "delivered"] = "placed"
    complete: bool = False
