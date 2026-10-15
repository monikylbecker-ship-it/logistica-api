
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Motorista
from app.schemas import MotoristaCreate, MotoristaResponse

router = APIRouter(
    prefix="/motoristas",
    tags=["Motoristas"],
)


@router.post(
    "/",
    response_model=MotoristaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_motorista(
    dados: MotoristaCreate,
    db: Session = Depends(get_db),
):
    # Verifica se a CNH já foi cadastrada.
    existente = (
        db.query(Motorista)
        .filter(Motorista.cnh == dados.cnh)
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um motorista com essa CNH.",
        )

    motorista = Motorista(**dados.model_dump())

    db.add(motorista)

    try:
        db.commit()
        db.refresh(motorista)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não foi possível cadastrar o motorista.",
        )

    return motorista


@router.get("/", response_model=list[MotoristaResponse])
def listar_motoristas(
    db: Session = Depends(get_db),
):
    return db.query(Motorista).order_by(Motorista.id).all()
