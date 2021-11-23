import json

from app.api import crud


def test_create_article(client, monkeypatch):
    test_request_payload = {"username": "test username", "text": "test text"}
    test_response_payload = {"id": 1, "username": "test username",
                             "text": "test text", "version": 0}

    async def mock_post(payload):
        return {"id": 1, "version": 0}

    monkeypatch.setattr(crud, "crete_article", mock_post)

    response = client.post("/articles/",
                           data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_article_invalid_json(client):
    response = client.post("/articles/",
                           data=json.dumps(
                               {"username": "test username invalid"}))
    assert response.status_code == 422


def test_read_article(client, monkeypatch):
    test_data = {"id": 1, "username": "test username", "text": "test text",
                 "version": 0}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = client.get("/articles/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_article_incorrect_id(client, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = client.get("/articles/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"


def test_read_all_articles(client, monkeypatch):
    test_data = [
        {"username": "test username 1", "text": "test text 1", "id": 1,
         "version": 0},
        {"username": "test username 2", "text": "test text 2", "id": 2,
         "version": 0},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = client.get("/articles/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_mock_update_article(client, monkeypatch):
    test_update_data = {"username": "test username update",
                        "text": "test text update", "id": 1, "version": 1,
                        "detail": f"Successfully updated article, new version: {1}"}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_update(payload):
        return {"id": 1, "username": "test username update",
                "text": "test text update", "version": 1}

    monkeypatch.setattr(crud, "update", mock_update)

    response = client.put("/articles/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


def test_direct_update_article(client):
    response = client.post("/articles/", data=json.dumps(
        {"username": "string", "text": "string"}))
    article_id = response.json()["id"]

    test_data = {"username": "test username update lock",
                 "text": "test text update lock", "id": article_id}
    test_update_data = {"username": "test username update lock",
                        "text": "test text update lock", "id": article_id,
                        "version": 1,
                        "detail": f"Successfully updated article, new version: {1}"}

    response = client.put(f"/articles/{article_id}/",
                          data=json.dumps(test_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


def test_optimistic_lock(client):
    # Create optimistic postgres lock while two request\users change one article

    # create article
    response = client.post("/articles/", data=json.dumps(
        {"username": "string", "text": "string"}))

    response = response.json()
    article_id = response["id"]
    user1_ver = response["version"]
    test_data_1 = {"username": "test username update lock by user 1",
                   "text": "test text update lock by user 1", "id": article_id,
                   "version": user1_ver}

    # say second user make call
    test_data_2 = {"username": "test username update lock by user 2",
                   "text": "test text update lock by user 2", "id": article_id}
    response_2 = client.put(f"/articles/{article_id}/",
                            data=json.dumps(test_data_2))

    # return to first user call
    response_1 = client.put(f"/articles/{article_id}/",
                            data=json.dumps(test_data_1))

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    assert response_1.json()["id"] == response_2.json()["id"]
    assert response_1.json()["version"] != response_2.json()["version"]
