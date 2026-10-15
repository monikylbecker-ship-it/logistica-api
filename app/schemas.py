
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StatusMotorista(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"


class StatusEntrega(str, Enum):
    PENDENTE = "Pendente"
    EM_TRANSITO = "Em Trânsito"
    ENTREGUE = "Entregue"


class MotoristaCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=150)
    cnh: str = Field(min_length=1, max_length=30)
    telefone: str = Field(min_length=8, max_length=20)
    status: StatusMotorista = StatusMotorista.ATIVO


class MotoristaResponse(BaseModel):
    id: int
    nome: str
    cnh: str
    telefone: str
    status: StatusMotorista

    model_config = ConfigDict(from_attributes=True)


class EntregaCreate(BaseModel):
    descricao_carga: str = Field(min_length=2, max_length=255)
    origem: str = Field(min_length=2, max_length=255)
    destino: str = Field(min_length=2, max_length=255)
    motorista_id: Optional[int] = Field(default=None, gt=0)


class EntregaResponse(BaseModel):
    id: int
    descricao_carga: str
    origem: str
    destino: str
    status: StatusEntrega
    motorista_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AtualizarStatus(BaseModel):
    status: StatusEntrega


class AtribuirMotorista(BaseModel):
    motorista_id: int = Field(gt=0)
