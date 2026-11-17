from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models import SessionLocal, Usuario, Dispositivo, Emprestimo, init_db

app = FastAPI(title="MVP Controle de Dispositivos Educacionais - P.E.I. Tercio Moraes")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()
    db = SessionLocal()
    if not db.query(Usuario).first():
        hash_senha = pwd_context.hash("escola2026")
        db.add(Usuario(nome="Estagiario Lucas", email="lucas.ti@escola.sp.gov.br", senha_hash=hash_senha))
        for i in range(1, 26):
            st = "ativo"
            obs = None
            if i in (16, 17):
                st = "emprestado"
            elif i == 18:
                st = "inservivel"
                obs = "Conector USB-C danificado"
            elif i in (19, 20):
                st = "gabinete_carregamento"
            db.add(Dispositivo(numero_identificacao=i, categoria="tablet", status_atual=st, observacao=obs))
        db.commit()
    db.close()

class DispositivoCreate(BaseModel):
    numero_identificacao: int = Field(..., ge=1, le=500)
    categoria: str = Field(..., pattern="^(tablet|chromebook|notebook)$")
    status_atual: str = Field(default="ativo", pattern="^(ativo|gabinete_carregamento|inservivel)$")
    observacao: Optional[str] = Field(default=None, max_length=500)

class LoteRequest(BaseModel):
    numeros: List[int] = Field(..., min_length=1)
    categoria: str = Field(default="tablet")
    acao: str = Field(..., pattern="^(emprestar|devolver|carregando|inservivel)$")
    nome_professor: Optional[str] = Field(default=None, max_length=100)
    turma: Optional[str] = Field(default=None, max_length=30)
    observacao: Optional[str] = Field(default=None, max_length=500)

@app.get("/")
def ler_interface():
    return FileResponse("static/index.html")

@app.get("/api/dispositivos")
def listar_dispositivos(categoria: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Dispositivo)
    if categoria and categoria != "todos":
        query = query.filter(Dispositivo.categoria == categoria)
    itens = query.order_by(Dispositivo.numero_identificacao).all()
    resumo = {
        "ativo": sum(1 for d in itens if d.status_atual == "ativo"),
        "emprestado": sum(1 for d in itens if d.status_atual == "emprestado"),
        "gabinete_carregamento": sum(1 for d in itens if d.status_atual == "gabinete_carregamento"),
        "inservivel": sum(1 for d in itens if d.status_atual == "inservivel"),
    }
    return {"resumo": resumo, "dispositivos": itens}

@app.post("/api/dispositivos", status_code=status.HTTP_201_CREATED)
def cadastrar_dispositivo(dados: DispositivoCreate, db: Session = Depends(get_db)):
    existente = db.query(Dispositivo).filter_by(
        categoria=dados.categoria, numero_identificacao=dados.numero_identificacao
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Dispositivo ja cadastrado nesta categoria.")
    novo = Dispositivo(**dados.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.post("/api/movimentacoes/lote")
def movimentar_lote(dados: LoteRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).first()
    aparelhos = db.query(Dispositivo).filter(
        Dispositivo.categoria == dados.categoria,
        Dispositivo.numero_identificacao.in_(dados.numeros)
    ).all()

    if len(aparelhos) != len(dados.numeros):
        raise HTTPException(status_code=404, detail="Um ou mais dispositivos nao foram encontrados.")

    if dados.acao == "emprestar":
        if not dados.nome_professor or not dados.turma:
            raise HTTPException(status_code=422, detail="Professor e turma sao obrigatorios para emprestimo.")
        for ap in aparelhos:
            if ap.status_atual != "ativo":
                raise HTTPException(status_code=409, detail=f"Aparelho {ap.numero_identificacao} indisponivel ({ap.status_atual}).")
            ap.status_atual = "emprestado"
            db.add(Emprestimo(
                id_dispositivo=ap.id_dispositivo,
                id_usuario=usuario.id_usuario,
                nome_professor=dados.nome_professor.strip(),
                turma=dados.turma.strip()
            ))
    elif dados.acao == "inservivel":
        if not dados.observacao:
            raise HTTPException(status_code=422, detail="Observacao tecnica obrigatoria ao marcar como inservivel.")
        for ap in aparelhos:
            ap.status_atual = "inservivel"
            ap.observacao = dados.observacao.strip()
    else:
        novo_status = "ativo" if dados.acao == "devolver" else "gabinete_carregamento"
        for ap in aparelhos:
            ap.status_atual = novo_status
            emp_aberto = db.query(Emprestimo).filter_by(
                id_dispositivo=ap.id_dispositivo, data_devolucao=None
            ).first()
            if emp_aberto:
                emp_aberto.data_devolucao = datetime.utcnow()

    db.commit()
    return {"mensagem": f"Lote de {len(aparelhos)} aparelhos atualizado com sucesso."}
