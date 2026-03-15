import re
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

class LogisticsType(str, Enum):
    LAND = "TERRESTRE"
    MARITIME = "MARITIMO"

class ClientBase(BaseModel):
    name: str = Field(min_length=1)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    name: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    model_config = {"from_attributes": True}

class ProductBase(BaseModel):
    name: str = Field(min_length=1)
    logistics_type: Optional[LogisticsType] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    logistics_type: Optional[LogisticsType] = None

class ProductResponse(ProductBase):
    id: int
    model_config = {"from_attributes": True}

class WarehouseBase(BaseModel):
    name: str = Field(min_length=1)
    location: Optional[str] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class WarehouseResponse(WarehouseBase):
    id: int
    model_config = {"from_attributes": True}

class PortBase(BaseModel):
    name: str = Field(min_length=1)
    is_international: bool = False
    location: Optional[str] = None

class PortCreate(PortBase):
    pass

class PortUpdate(BaseModel):
    name: Optional[str] = None
    is_international: Optional[bool] = None
    location: Optional[str] = None

class PortResponse(PortBase):
    id: int
    model_config = {"from_attributes": True}

class ShipmentCreate(BaseModel):
    logistics_type: LogisticsType
    tracking_number: str = Field(pattern=r"^[A-Za-z0-9]{10}$")
    product_quantity: int = Field(gt=0)
    delivery_date: datetime
    shipping_price: float = Field(gt=0)

    client_id: int
    product_id: int

    # Land specific
    vehicle_plate: Optional[str] = None
    warehouse_id: Optional[int] = None

    # Maritime specific
    fleet_number: Optional[str] = None
    port_id: Optional[int] = None

    @field_validator("vehicle_plate")
    @classmethod
    def validate_plate(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not re.match(r"^[A-Z]{3}[0-9]{3}$", v):
                raise ValueError("La placa debe seguir el formato AAA123")
        return v

    @field_validator("fleet_number")
    @classmethod
    def validate_fleet(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not re.match(r"^[A-Z]{3}[0-9]{4}[A-Z]$", v):
                raise ValueError("El numero de flota debe ser AAA1234A (3 letras + 4 numeros + 1 letra)")
        return v

    @model_validator(mode="after")
    def validate_fields_by_type(self):
        if self.logistics_type == LogisticsType.LAND:
            if not self.vehicle_plate:
                raise ValueError("vehicle_plate is required for land logistics")
            if not self.warehouse_id:
                raise ValueError("warehouse_id is required for land logistics")
        elif self.logistics_type == LogisticsType.MARITIME:
            if not self.fleet_number:
                raise ValueError("fleet_number is required for maritime logistics")
            if not self.port_id:
                raise ValueError("port_id is required for maritime logistics")
        return self

class ShipmentUpdate(BaseModel):
    product_quantity: Optional[int] = Field(default=None, gt=0)
    delivery_date: Optional[datetime] = None
    shipping_price: Optional[float] = Field(default=None, gt=0)
    vehicle_plate: Optional[str] = None
    warehouse_id: Optional[int] = None
    fleet_number: Optional[str] = None
    port_id: Optional[int] = None

    @field_validator("vehicle_plate")
    @classmethod
    def validate_plate(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not re.match(r"^[A-Z]{3}[0-9]{3}$", v):
                raise ValueError("Plate must follow the format AAA123")
        return v

    @field_validator("fleet_number")
    @classmethod
    def validate_fleet(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not re.match(r"^[A-Z]{3}[0-9]{4}[A-Z]$", v):
                raise ValueError("Fleet number must follow the format AAA1234A")
        return v

class ShipmentResponse(BaseModel):
    id: int
    logistics_type: str
    tracking_number: str
    product_quantity: int
    registration_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    shipping_price: float
    final_price: Optional[float] = None
    vehicle_plate: Optional[str] = None
    warehouse_id: Optional[int] = None
    fleet_number: Optional[str] = None
    port_id: Optional[int] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    model_config = {"from_attributes": True}

class UserRegister(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: Optional[datetime] = None 
    model_config = {"from_attributes": True}