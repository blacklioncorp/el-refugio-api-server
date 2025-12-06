from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category = Column(String)
    is_active = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(String) # Ej: "Mesa 1" o "Domicilio"
    status = Column(String, default="PENDING") # PENDING, COOKING, READY...
    total = Column(Float, default=0.0)
    items = Column(JSON) # Guardaremos el detalle como JSON por simplicidad inicial