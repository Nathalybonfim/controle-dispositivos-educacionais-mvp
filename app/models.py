from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./dispositivos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuario"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False, default="estagiario_ti")
    ativo = Column(Boolean, default=True, nullable=False)

class Dispositivo(Base):
    __tablename__ = "dispositivo"
    id_dispositivo = Column(Integer, primary_key=True, index=True)
    numero_identificacao = Column(Integer, nullable=False)
    categoria = Column(String(30), nullable=False)
    status_atual = Column(String(30), nullable=False, default="ativo")
    observacao = Column(String(500), nullable=True)

    __table_args__ = (
        UniqueConstraint("categoria", "numero_identificacao", name="uq_categoria_numero"),
    )

class Emprestimo(Base):
    __tablename__ = "emprestimo"
    id_emprestimo = Column(Integer, primary_key=True, index=True)
    id_dispositivo = Column(Integer, ForeignKey("dispositivo.id_dispositivo"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    nome_professor = Column(String(100), nullable=False)
    turma = Column(String(30), nullable=False)
    data_retirada = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_devolucao = Column(DateTime, nullable=True)

    dispositivo = relationship("Dispositivo")
    usuario = relationship("Usuario")

def init_db():
    Base.metadata.create_all(bind=engine)
