from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company = Column(String)

    shipments = relationship("Shipment", back_populates="client")


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    logistics_type = Column(String)  # 'LAND' or 'MARITIME'


class Warehouse(Base): 
    __tablename__ = "warehouse"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)


class Port(Base):
    __tablename__ = "port"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_international = Column(Boolean, default=False)
    location = Column(String)


class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(10), unique=True, index=True, nullable=False) 
    logistics_type = Column(String, nullable=False) # 'LAND' or 'MARITIME'

    product_quantity = Column(Integer, nullable=False)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    delivery_date = Column(DateTime)
    shipping_price = Column(Float, nullable=False)
    final_price = Column(Float)

    vehicle_plate = Column(String(6), nullable=True) 
    fleet_number = Column(String(8), nullable=True) 

    client_id = Column(Integer, ForeignKey("client.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"), nullable=True)
    port_id = Column(Integer, ForeignKey("port.id"), nullable=True)

    client = relationship("Client", back_populates="shipments")
    product = relationship("Product")

    @property
    def client_name(self) -> str | None:
        return self.client.name if self.client else None

    @property
    def product_name(self) -> str | None:
        return self.product.name if self.product else None


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())