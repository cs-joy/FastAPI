from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    model_config ={"extra": "forbid"}

class UserInDB(User):
    password: str
    is_disabled: bool = False
    model_config ={"extra": "forbid"}

class Product(BaseModel):
    name: str
    category: list | None = None
    brand: str | None = None
    tax: float  = 0.034
    price: float
    status: str
    tags: list | None = list()
    created_at: str
    updated_at: str | None = None
    model_config ={"extra": "forbid"}