from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.utils import is_valid_datetime
from tracko.domain.task.task_enums import TaskStatusEnum


def test_create_task_returns_created(client: TestClient, token_admin: str):
    response = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'title': 'Test title',
            'description': 'Test description',
            'start_date': '2026-01-01T00:00:00.000Z',
            'end_date': '2026-01-02T00:00:00.000Z',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['id']
    assert data['title'] == 'Test title'
    assert data['description'] == 'Test description'
    assert data['status'] == TaskStatusEnum.TODO
    assert is_valid_datetime(data['created_at'])
    assert is_valid_datetime(data['modified_at'])
