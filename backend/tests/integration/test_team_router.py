from http import HTTPStatus
from uuid import uuid4

from tracko.domain.user.user_enums import UserRoleEnum


def test_create_team(client, token_admin):
    response = client.post(
        "/teams/",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "name": "Team A",
            "description": "desc",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == "Team A"


def test_read_many_teams(client, token_admin):
    response = client.get(
        "/teams/",
        headers={"Authorization": f"Bearer {token_admin}"},
        params={"offset": 0, "limit": 10},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert "teams" in data
    assert "total" in data


def test_read_one_team(client, token_admin):
    create = client.post(
        "/teams/",
        headers={"Authorization": f"Bearer {token_admin}"},
        json={
            "name": "Team One",
            "description": "desc",
        },
    )

    team_id = create.json()["id"]

    response = client.get(
        f"/teams/{team_id}",
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == team_id
