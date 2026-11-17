# 📱 Sistema de Controle e Rastreamento de Dispositivos Educacionais (MVP)
![CI Status](https://github.com)


Aplicação Web Responsiva (*Mobile-First*) desenvolvida para substituir o controle manual em caderno físico realizado pelos estagiários de TI da **Escola Estadual P.E.I. Reverendo Tércio Moraes Pereira**, alinhada ao [**ODS 4 — Educação de Qualidade (ONU Brasil)**](https://un.org).

## 📑 Sumário Navegável
* [🎯 Objetivo e Diferencial](#-objetivo-e-diferencial)
* [🏗️ Arquitetura e Stack Tecnológica](#️-arquitetura-e-stack-tecnológica)
* [📂 Estrutura do Projeto](#-estrutura-do-projeto)
* [🚀 Como Executar Localmente](#-como-executar-localmente)
* [🧪 Testes e Integração Contínua (CI)](#-testes-e-integração-contínua-ci)

---

## 🎯 Objetivo e Diferencial
Agilizar o empréstimo, a devolução e o controle patrimonial de **tablets, Chromebooks e notebooks** durante os horários de pico nas trocas de aula por meio de uma **grade numérica tátil de seleção em lote** e controle visual imediato de 4 status operacionais:
* ✅ **Ativo** (Disponível para uso em sala)
* ➡️ **Emprestado** (Vinculado a professor e turma)
* ⚡ **No Gabinete de Carregamento** (Em ciclo de recarga)
* ⚠️ **Inservível** (Bloqueado para manutenção com registro de defeito)

---

## 🏗️ Arquitetura e Stack Tecnológica
* **Arquitetura:** Cliente-Servidor em 3 Camadas (SPA Responsiva + API RESTful + Banco Relacional).
* **Back-end:** [**Python 3.12**](https://python.org) com [**FastAPI**](https://tiangolo.com), [**Uvicorn**](https://uvicorn.org), [**SQLAlchemy 2.0+**](https://sqlalchemy.org) e [**Pydantic**](https://pydantic.dev).
* **Front-end:** HTML5, CSS3 e JavaScript ES6+ com diretrizes de acessibilidade [**WCAG 2.1 AA**](https://w3.org).
* **Segurança:** Autenticação JWT ([**PyJWT**](https://readthedocs.io)) e hash de senhas com `bcrypt` ([**Passlib**](https://readthedocs.io)), seguindo recomendações do [**OWASP Top 10**](https://owasp.org).
* **Banco de Dados:** [**PostgreSQL 16**](https://postgresql.org) (hospedado via [**Supabase**](https://supabase.com)) e SQLite para testes locais.
* **Qualidade & CI:** [**Pytest**](https://pytest.org), [**HTTPX**](https://python-httpx.org) e [**GitHub Actions**](https://github.com).

---

## 📂 Estrutura do Projeto
* [`app/main.py`](app/main.py) — Rotas da API RESTful, regras de lote e servir a interface web.
* [`app/models.py`](app/models.py) — Modelos relacionais (`Usuario`, `Dispositivo` e `Emprestimo`).
* [`static/index.html`](static/index.html) — Interface Web Responsiva (*Mobile-First*).
* [`tests/test_api.py`](tests/test_api.py) — Suíte de testes unitários e de integração (`Pytest`).
* [`.github/workflows/ci.yml`](.github/workflows/ci.yml) — Pipeline automatizado de Integração Contínua.

---

## 🚀 Como Executar Localmente
1. Clone este repositório:
   ```bash
git clone https://github.com
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Acesse no navegador:
   * **Interface Web:** `http://127.0.0.1:8000`
* **Documentação Interativa da API (Swagger):** `http://127.0.0`

---

## 🧪 Testes e Integração Contínua (CI)
Para executar os testes automatizados localmente, utilize o comando:
```bash
pytest -v
```
