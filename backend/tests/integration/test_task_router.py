from http import HTTPStatus


def test_create_task(client, token_admin):
    response = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'title': 'Task Integration',
            'description': 'desc',
            'start_date': None,
            'end_date': None,
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['id'] is not None
    assert data['title'] == 'Task Integration'


def test_read_tasks(client, token_admin):
    response = client.get(
        '/tasks/',
        headers={'Authorization': f'Bearer {token_admin}'},
        params={'offset': 0, 'limit': 10},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'tasks' in data
    assert 'total' in data


def test_read_one_task(client, token_admin):
    # cria task
    create = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'title': 'Task One',
            'description': 'desc',
            'start_date': None,
            'end_date': None,
        },
    )

    # le task
    task_id = create.json()['id']

    response = client.get(
        f'/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token_admin}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == task_id


def test_update_task(client, token_admin):
    # cria task
    create = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'title': 'Task Update',
            'description': 'desc',
        },
    )

    # atualiza task
    task_id = create.json()['id']

    response = client.patch(
        f'/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={'status': 'done'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['status'] == 'done'


def test_delete_task(client, token_admin):
    # cria task
    create = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token_admin}'},
        json={
            'title': 'Task Delete',
            'description': 'desc',
            'start_date': None,
            'end_date': None,
        },
    )

    # deleta task
    task_id = create.json()['id']

    response = client.delete(
        f'/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token_admin}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
