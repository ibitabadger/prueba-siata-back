from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from models import User
from schemas import WarehouseCreate, WarehouseResponse, WarehouseUpdate
from services.warehouse_service import (
    create_warehouse,
    delete_warehouse as delete_warehouse_svc,
    get_warehouse,
    list_warehouses,
    update_warehouse,
)

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.get("", response_model=list[WarehouseResponse])
@router.get("/", response_model=list[WarehouseResponse])
def list_warehouses_endpoint(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list_warehouses(db)


@router.get("/{warehouse_id:int}", response_model=WarehouseResponse)
def get_warehouse_endpoint(
    warehouse_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    warehouse = get_warehouse(warehouse_id, db)
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bodega no encontrada")
    return warehouse


@router.post("", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse_endpoint(
    body: WarehouseCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return create_warehouse(body.model_dump(), db)


@router.put("/{warehouse_id:int}", response_model=WarehouseResponse)
def update_warehouse_endpoint(
    warehouse_id: int,
    body: WarehouseUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    warehouse = update_warehouse(warehouse_id, body.model_dump(exclude_unset=True), db)
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bodega no encontrada")
    return warehouse


@router.delete("/{warehouse_id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse_endpoint(
    warehouse_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    if not delete_warehouse_svc(warehouse_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bodega no encontrada")
