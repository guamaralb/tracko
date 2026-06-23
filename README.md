# Tracko - Sistema de Gerenciamento de Tarefas

## 1. Membros do Grupo

* Gustavo Amaral Bernardino
* José Gabriel Vieira de Souza
* Wesley Marques Daniel Chaves

---

## 2. Explicação do Sistema

O **Tracko** é um sistema completo de gerenciamento de tarefas desenvolvido para auxiliar usuários na organização de suas atividades diárias. O projeto evoluiu de uma aplicação CLI para uma arquitetura robusta de **Client-Server**, composta por:

* **Backend:** API RESTful construída com FastAPI, seguindo princípios de Clean Architecture, com persistência de dados e autenticação segura via JWT.
* **Frontend:** Interface moderna desenvolvida em React, focada em usabilidade e design responsivo.

### Funcionalidades principais:

* **Autenticação:** Cadastro e login de usuários com tokens de acesso.
* **Gerenciamento de Tarefas:** Criação, listagem, atualização de status (`todo`, `in_progress`, `done`) e exclusão.
* **Segurança:** Isolamento de dados por usuário (cada usuário visualiza e gerencia apenas suas próprias tarefas).
* **Filtros:** Busca inteligente de tarefas.

---

## 3. Tecnologias Utilizadas

### Backend

* **Linguagem:** Python 3.13
* **Framework:** FastAPI
* **Banco de Dados/ORM:** SQLAlchemy
* **Autenticação:** JWT (JSON Web Tokens)
* **Gerenciamento de Dependências:** Poetry

### Frontend

* **Framework:** React com Vite
* **Linguagem:** TypeScript
* **Comunicação:** Axios (Consumo da API REST)

### Qualidade e Testes

* **Testes:** Pytest (Testes de Unidade e Integração)
* **Code Quality:** Ruff (Linter e Formatter)

### Uso de Inteligência Artificial

* Assistência no design da arquitetura de **Unit of Work**.
* Auxílio na implementação de *Dependency Injection* e *Factories*.
* Suporte no tratamento de exceções customizadas e depuração de erros de integração (FastAPI/React).
* Automação de tarefas (linter/formatter) e configuração de CI/CD.

---

## 4. Como Executar o Projeto Localmente

### Pré-requisitos

Certifique-se de ter o [Poetry](https://python-poetry.org/) e o [Node.js](https://nodejs.org/) instalados em sua máquina.

### Backend

1. Navegue até a pasta `backend`: `cd backend`
2. Instale as dependências: `poetry install`
3. Inicie o servidor: `poetry run task run`

### Frontend

1. Navegue até a pasta `frontend`: `cd frontend`
2. Instale as dependências: `npm install`
3. Inicie a interface: `npm run dev`

### Execução de Testes

Para rodar a suíte de testes (Backend):

* Na pasta `backend`: `poetry run task test`

### Manutenção de Código (Linter e Formatter)

* Para formatar o código automaticamente: `poetry run task format`
* Para rodar o linter: `poetry run task lint`

---
