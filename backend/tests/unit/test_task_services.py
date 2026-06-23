from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

# Importe os seus modelos, schemas e serviços
from tracko.domain.task.task_enums import TaskStatusEnum
from tracko.domain.task.task_models import TaskModel
from tracko.domain.task.task_schemas import (
    FilterTaskSchema,
    TaskCreateSchema,
    TaskUpdateSchema,
)
from tracko.domain.task.task_services import (
    task_service_create,
    task_service_delete,
    task_service_read_many,
    task_service_read_one,
    task_service_update,
)
from tracko.domain.user.user_models import UserModel

NOT_FOUND_CODE = 404


# --- FIXTURES (Dados falsos para usar nos testes) ---
@pytest.fixture
def mock_user():
    """Retorna um usuário falso logado"""
    user = MagicMock(spec=UserModel)
    user.id = uuid4()
    user.email = "teste@teste.com"
    return user


@pytest.fixture
def mock_uow():
    """Retorna um UnitOfWork falso com o repositório mockado"""
    uow = MagicMock()
    # Limpa as chamadas antes de cada teste
    uow.tasks.reset_mock()
    return uow


@pytest.fixture
def dummy_task(mock_user):
    """Retorna uma tarefa falsa vinda do banco de dados"""
    task = MagicMock(spec=TaskModel)
    task.id = uuid4()
    task.title = "Estudar Pytest"
    task.description = "Fazer testes de unidade"
    task.status = TaskStatusEnum.TODO
    task.user_id_creator = mock_user.id
    task.start_date = datetime.now(timezone.utc)
    task.end_date = None
    task.created_at = datetime.now(timezone.utc)
    task.modified_at = datetime.now(timezone.utc)
    return task


# --- TESTES DE CRIAÇÃO (CREATE) ---
def test_task_service_create_success(mock_uow, mock_user, dummy_task):
    # 1. Prepara os dados de entrada
    schema_in = TaskCreateSchema(
        title="Estudar Pytest",
        description="Fazer testes de unidade"
    )

    mock_uow.tasks.add.return_value = dummy_task

    # 3. Chama o serviço
    result = task_service_create(uow=mock_uow, current_user=mock_user,
                                 data=schema_in)

    # 4. Verificações (Asserts)
    mock_uow.tasks.add.assert_called_once()  # Garante que tentou salvar
    assert result.title == "Estudar Pytest"
    assert result.id == dummy_task.id


# --- TESTES DE LEITURA (READ MANY) ---
def test_task_service_read_many_success(mock_uow, mock_user, dummy_task):
    filter_schema = FilterTaskSchema(offset=0, limit=10)

    # Simula o banco retornando uma lista com 1 tarefa, e o total = 1
    mock_uow.tasks.get_many.return_value = ([dummy_task], 1)

    result = task_service_read_many(
        uow=mock_uow, current_user=mock_user, filter=filter_schema
    )

    mock_uow.tasks.get_many.assert_called_once_with(user_id=mock_user.id,
                                                    filter=filter_schema)
    assert result.total == 1
    assert len(result.tasks) == 1
    assert result.tasks[0].id == dummy_task.id


# --- TESTES DE LEITURA ÚNICA (READ ONE) ---
def test_task_service_read_one_success(mock_uow, mock_user, dummy_task):
    mock_uow.tasks.get_one.return_value = dummy_task

    result = task_service_read_one(
        uow=mock_uow, current_user=mock_user, task_id=dummy_task.id
    )

    mock_uow.tasks.get_one.assert_called_once_with(user_id=mock_user.id,
                                                   task_id=dummy_task.id)
    assert result.id == dummy_task.id


def test_task_service_read_one_not_found(mock_uow, mock_user):
    # Simula o banco não encontrando a tarefa (retornando None)
    mock_uow.tasks.get_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service_read_one(uow=mock_uow, current_user=mock_user,
                              task_id=uuid4())

    assert exc_info.value.status_code == NOT_FOUND_CODE


# --- TESTES DE ATUALIZAÇÃO (UPDATE) ---
def test_task_service_update_success(mock_uow, mock_user, dummy_task):
    update_data = TaskUpdateSchema(status=TaskStatusEnum.DONE)
    dummy_task.status = TaskStatusEnum.DONE  # Atualiza o dummy para o mock

    mock_uow.tasks.update.return_value = dummy_task

    result = task_service_update(
        uow=mock_uow, current_user=mock_user, task_id=dummy_task.id,
        data=update_data
    )

    mock_uow.tasks.update.assert_called_once_with(
        user_id=mock_user.id, task_id=dummy_task.id, status=TaskStatusEnum.DONE
    )
    assert result.status == TaskStatusEnum.DONE


def test_task_service_update_not_found(mock_uow, mock_user):
    update_data = TaskUpdateSchema(status=TaskStatusEnum.DONE)

    # Simula a tarefa não pertencendo ao usuário (retorna None na atualização)
    mock_uow.tasks.update.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service_update(
            uow=mock_uow, current_user=mock_user, task_id=uuid4(),
            data=update_data
        )

    assert exc_info.value.status_code == NOT_FOUND_CODE


# --- TESTES DE EXCLUSÃO (DELETE) ---
def test_task_service_delete_success(mock_uow, mock_user, dummy_task):
    # Primeiro a função busca a tarefa para ver se existe
    mock_uow.tasks.get_one.return_value = dummy_task

    # Chama o serviço
    task_service_delete(
        uow=mock_uow, current_user=mock_user, task_id=dummy_task.id)

    # Garante que buscou E que deletou
    mock_uow.tasks.get_one.assert_called_once()
    mock_uow.tasks.delete.assert_called_once_with(dummy_task)


def test_task_service_delete_not_found(mock_uow, mock_user):
    # Simula a busca falhando
    mock_uow.tasks.get_one.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service_delete(
            uow=mock_uow, current_user=mock_user, task_id=uuid4())

    assert exc_info.value.status_code == NOT_FOUND_CODE
    # Garante que NUNCA chamou o delete se a tarefa não existe
    mock_uow.tasks.delete.assert_not_called()
