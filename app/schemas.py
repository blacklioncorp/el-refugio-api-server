from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    price: float
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    notes: Optional[str] = None

class OrderCreate(BaseModel):
    table_id: str
    items: List[OrderItem]

class Order(OrderCreate):
    id: int
    status: str
    total: float
    class Config:
        orm_mode = True