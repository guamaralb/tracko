from http import HTTPStatus


# --- 1. Teste de Integração: Fluxo de Criação e Leitura de Time ---
def test_integration_create_and_read_team(client, token_admin, session):
    # 1. Cria o time
    payload = {"name": "Integration Team", "description": "Testing full flow"}
    create_response = client.post(
        "/teams/",
        json=payload,
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert create_response.status_code == HTTPStatus.CREATED
    team_id = create_response.json()["id"]

    # 2. Busca o time recém-criado
    read_response = client.get(
        f"/teams/{team_id}",
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert read_response.status_code == HTTPStatus.OK
    assert read_response.json()["id"] == team_id
    assert read_response.json()["name"] == "Integration Team"
