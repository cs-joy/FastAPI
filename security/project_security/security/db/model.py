from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import random
import string
import secrets

Base = declarative_base()

def generate_random_string(length: int):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

class UserDB(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=generate_random_string(5))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_disabled = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ProductsDB(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, default=generate_random_string(8))
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    tax = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    tags = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())