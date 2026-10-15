
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Entrega, Motorista
from app.schemas import (
    AtribuirMotorista,
    AtualizarStatus,
    EntregaCreate,
    EntregaResponse,
    StatusEntrega,
)

router = APIRouter(
    prefix="/entregas",
    tags=["Entregas"],
)


def buscar_entrega(db: Session, entrega_id: int) -> Entrega:
    """Busca uma entrega ou retorna HTTP 404."""
    entrega = db.get(Entrega, entrega_id)

    if entrega is None:
        raise HTTPException(
            status_code=404,
            detail="Entrega não encontrada.",
        )

    return entrega


@router.post(
    "/",
    response_model=EntregaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_entrega(
    dados: EntregaCreate,
    db: Session = Depends(get_db),
):
    # Se o motorista foi informado, valida sua existência.
    if dados.motorista_id is not None:
        motorista = db.get(Motorista, dados.motorista_id)

        if motorista is None:
            raise HTTPException(
                status_code=404,
                detail="Motorista não encontrado.",
            )

        if motorista.status != "ativo":
            raise HTTPException(
                status_code=400,
                detail="Não é possível atribuir motorista inativo.",
            )

    entrega = Entrega(**dados.model_dump())

    db.add(entrega)
    db.commit()
    db.refresh(entrega)

    return entrega


@router.get("/", response_model=list[EntregaResponse])
def listar_entregas(
    status_entrega: StatusEntrega | None = Query(
        default=None,
        alias="status",
        description="Filtrar por Pendente, Em Trânsito ou Entregue",
    ),
    db: Session = Depends(get_db),
):
    consulta = db.query(Entrega)

    if status_entrega is not None:
        consulta = consulta.filter(
            Entrega.status == status_entrega.value
        )

    return consulta.order_by(Entrega.id).all()


@router.patch(
    "/{entrega_id}/status",
    response_model=EntregaResponse,
)
def atualizar_status(
    entrega_id: int,
    dados: AtualizarStatus,
    db: Session = Depends(get_db),
):
    entrega = buscar_entrega(db, entrega_id)

    # Regra simples de progressão do fluxo logístico.
    transicoes = {
        "Pendente": {"Em Trânsito"},
        "Em Trânsito": {"Entregue"},
        "Entregue": set(),
    }

    novo_status = dados.status.value

    if novo_status == entrega.status:
        return entrega

    if novo_status not in transicoes[entrega.status]:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Transição inválida: {entrega.status} "
                f"para {novo_status}."
            ),
        )

    entrega.status = novo_status

    db.commit()
    db.refresh(entrega)

    return entrega


@router.patch(
    "/{entrega_id}/motorista",
    response_model=EntregaResponse,
)
def atribuir_motorista(
    entrega_id: int,
    dados: AtribuirMotorista,
    db: Session = Depends(get_db),
):
    entrega = buscar_entrega(db, entrega_id)
    motorista = db.get(Motorista, dados.motorista_id)

    if motorista is None:
        raise HTTPException(
            status_code=404,
            detail="Motorista não encontrado.",
        )

    if motorista.status != "ativo":
        raise HTTPException(
            status_code=400,
            detail="Não é possível atribuir motorista inativo.",
        )

    if entrega.status == "Entregue":
        raise HTTPException(
            status_code=400,
            detail="Não é possível atribuir motorista a uma entrega concluída.",
        )

    entrega.motorista_id = motorista.id

    db.commit()
    db.refresh(entrega)

    return entrega
