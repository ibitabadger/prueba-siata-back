from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from models import User
from schemas import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from services.exceptions import DuplicateError
from services.shipment_service import (
    create_shipment,
    delete_shipment as delete_shipment_svc,
    get_shipment,
    list_shipments,
    update_shipment,
)

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.get("", response_model=list[ShipmentResponse])
@router.get("/", response_model=list[ShipmentResponse])
def list_shipments_endpoint(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list_shipments(db)


@router.get("/{shipment_id:int}", response_model=ShipmentResponse)
def get_shipment_endpoint(
    shipment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    shipment = get_shipment(shipment_id, db)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
    return shipment


@router.post("", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment_endpoint(
    body: ShipmentCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    try:
        return create_shipment(body.model_dump(), db)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{shipment_id:int}", response_model=ShipmentResponse)
def update_shipment_endpoint(
    shipment_id: int,
    body: ShipmentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    shipment = update_shipment(shipment_id, body.model_dump(exclude_unset=True), db)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
    return shipment


@router.delete("/{shipment_id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment_endpoint(
    shipment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    if not delete_shipment_svc(shipment_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
