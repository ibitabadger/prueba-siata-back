from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from models import User
from schemas import PortCreate, PortResponse, PortUpdate
from services.port_service import (
    create_port,
    delete_port as delete_port_svc,
    get_port,
    list_ports,
    update_port,
)

router = APIRouter(prefix="/ports", tags=["ports"])


@router.get("", response_model=list[PortResponse])
@router.get("/", response_model=list[PortResponse])
def list_ports_endpoint(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list_ports(db)


@router.get("/{port_id:int}", response_model=PortResponse)
def get_port_endpoint(
    port_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    port = get_port(port_id, db)
    if not port:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puerto no encontrado")
    return port


@router.post("", response_model=PortResponse, status_code=status.HTTP_201_CREATED)
def create_port_endpoint(
    body: PortCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return create_port(body.model_dump(), db)


@router.put("/{port_id:int}", response_model=PortResponse)
def update_port_endpoint(
    port_id: int,
    body: PortUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    port = update_port(port_id, body.model_dump(exclude_unset=True), db)
    if not port:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puerto no encontrado")
    return port


@router.delete("/{port_id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_port_endpoint(
    port_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    if not delete_port_svc(port_id, db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Puerto no encontrado")
