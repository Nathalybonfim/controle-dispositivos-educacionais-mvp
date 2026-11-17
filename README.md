# controle-dispositivos-educacionais-mvp
MVP Web Responsivo (Python/FastAPI) para controle de empréstimo e status em lote de dispositivos educacionais na P.E.I. Reverendo Tércio Moraes Pereira.
# 📱 Sistema de Controle e Rastreamento de Dispositivos Educacionais (MVP)

Aplicação Web Responsiva (*Mobile-First*) desenvolvida para substituir o controle manual em caderno físico realizado pelos estagiários de TI da **Escola Estadual P.E.I. Reverendo Tércio Moraes Pereira**, alinhada ao **ODS 4 (Educação de Qualidade)**.

## 🎯 Objetivo e Diferencial
Agilizar o empréstimo, a devolução e o controle patrimonial de **tablets, Chromebooks e notebooks** durante os horários de pico nas trocas de aula por meio de uma **grade numérica tátil de seleção em lote** e controle visual imediato de 4 status operacionais:
* ✅ **Ativo** (Disponível para uso em sala)
* ➡️ **Emprestado** (Vinculado a professor e turma)
* ⚡ **No Gabinete de Carregamento** (Em ciclo de recarga)
* ⚠️ **Inservível** (Bloqueado para manutenção com registro de defeito)

## 🏗️ Arquitetura e Stack Tecnológica
* **Arquitetura:** Cliente-Servidor em 3 Camadas (SPA Responsiva + API RESTful + Banco Relacional).
* **Back-end:** Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.0+, Pydantic.
* **Front-end:** HTML5, CSS3, JavaScript ES6+ (acessibilidade WCAG 2.1 AA).
* **Segurança:** Autenticação JWT (`PyJWT`) e hash de senhas com `bcrypt` (`Passlib`).
* **Banco de Dados:** PostgreSQL 16 (Supabase) / SQLite (ambiente de testes).
* **Qualidade & CI:** Pytest, HTTPX e GitHub Actions.

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
