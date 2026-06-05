# TS-TP01

## 1. Membros do Grupo
- Gustavo Amaral Bernardino
- José Gabriel Vieira de Souza
- Wesley Marques Daniel Chaves


---

## 2. Explicação do Sistema

O sistema consiste em um **gerenciador de tarefas em linha de comando (CLI)**, que permite ao usuário organizar suas atividades do dia a dia.

### Funcionalidades principais:

* **Adicionar tarefa**
* **Listar tarefas**
* **Marcar tarefa como concluída**
* **Remover tarefa**
* **Filtrar tarefas**

---

## 3. Tecnologias Utilizadas

### Linguagem

* Python

### Estrutura

* Aplicação de linha de comando (CLI)

### Bibliotecas

* `argparse` (para leitura de comandos no terminal)
* `json` ou `sqlite3` (para persistência de dados)

### Testes

* `pytest`

### Versionamento

* Git
* GitHub

### Usos de Inteligência Artificial (Claude, copilot)
* Criação de mensagens de commit
* Ajuda com criação da lógica do Unit Of Work para gerenciamento de operações
* Ajuda com a interpretação e correção de mensagens de erro
* Ajuda com a configuração dos testes no pytest
* Realizar mudanças simples, mas que afetam um número grande de arquivos
    * Depois de aproximadamente 10 commits, decidimos adiconar o tipo de retorno a todas as funções
* Ajuda sobre uma forma elegante de gerenciar permissões (implementação de uma dependency factory)

## 4. Como Rodar
* Backend
    * Na pasta "backend":
        * Baixar poetry
            * pip install poetry
        * Rodar os comandos:
            * poetry lock
            * poetry install
            * poetry run task run
                * Esse comando roda o linter e o formater antes de rodar o backend
