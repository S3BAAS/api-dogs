from pydantic import BaseModel


class Dog(BaseModel):
    id: str | None = None
    name: str
    picture: str | None = None
    create_date: str | None = None
    is_adopted: bool
