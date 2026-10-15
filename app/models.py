
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Motorista(Base):
    __tablename__ = "motoristas"

    __table_args__ = (
        CheckConstraint(
            "status IN ('ativo', 'inativo')",
            name="ck_motorista_status",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False, index=True)
    cnh = Column(String(30), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=False)
    status = Column(
        String(10),
        nullable=False,
        default="ativo",
    )

    # Um motorista pode estar associado a várias entregas.
    entregas = relationship(
        "Entrega",
        back_populates="motorista",
    )


class Entrega(Base):
    __tablename__ = "entregas"

    __table_args__ = (
        CheckConstraint(
            "status IN ('Pendente', 'Em Trânsito', 'Entregue')",
            name="ck_entrega_status",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    descricao_carga = Column(String(255), nullable=False)
    origem = Column(String(255), nullable=False)
    destino = Column(String(255), nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="Pendente",
    )

    # O motorista pode ser definido posteriormente.
    motorista_id = Column(
        Integer,
        ForeignKey("motoristas.id", ondelete="SET NULL"),
        nullable=True,
    )

    motorista = relationship(
        "Motorista",
        back_populates="entregas",
    )
