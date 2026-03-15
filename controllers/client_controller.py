from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from models import User
from schemas import ClientCreate, ClientResponse, ClientUpdate
from services.exceptions import ConflictError
from services.client_service import (
    create_client,
    delete_client as delete_client_svc,
    get_client,
    list_clients,
    update_client,
)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientResponse])
def list_clients_endpoint(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list_clients(db)


@router.get("/{client_id}", response_model=ClientResponse)
def get_client_endpoint(
    client_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    client = get_client(client_id, db)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return client


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client_endpoint(
    body: ClientCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return create_client(body.model_dump(), db)


@router.put("/{client_id}", response_model=ClientResponse)
def update_client_endpoint(
    client_id: int,
    body: ClientUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    client = update_client(client_id, body.model_dump(exclude_unset=True), db)
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client_endpoint(
    client_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    try:
        if not delete_client_svc(client_id, db):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
