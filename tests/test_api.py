from fastapi.testclient import TestClient
from app.main import app

def test_listar_dispositivos_inicial():
    with TestClient(app) as client:
        resp = client.get("/api/dispositivos")
        assert resp.status_code == 200
        dados = resp.json()
        assert "resumo" in dados
        assert len(dados["dispositivos"]) >= 25

def test_emprestimo_em_lote_sucesso():
    with TestClient(app) as client:
        payload = {
            "numeros": list(range(1, 6)),
            "categoria": "tablet",
            "acao": "emprestar",
            "nome_professor": "Prof. Mariana",
            "turma": "2 D"
        }
        resp = client.post("/api/movimentacoes/lote", json=payload)
        assert resp.status_code == 200
        assert "atualizado com sucesso" in resp.json()["mensagem"]

def test_bloqueio_aparelho_inservivel():
    with TestClient(app) as client:
        payload = {
            "numeros": list(range(18, 19)),
            "categoria": "tablet",
            "acao": "emprestar",
            "nome_professor": "Prof. Carlos",
            "turma": "9 A"
        }
        resp = client.post("/api/movimentacoes/lote", json=payload)
        assert resp.status_code == 409
        assert "indisponivel" in resp.json()["detail"]

def test_devolucao_e_gabinete_carregamento():
    with TestClient(app) as client:
        resp = client.post("/api/movimentacoes/lote", json={
            "numeros": list(range(1, 6)),
            "categoria": "tablet",
            "acao": "carregando"
        })
        assert resp.status_code == 200
