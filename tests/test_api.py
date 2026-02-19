from datetime import datetime, timezone

def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_register_user_creates_new_user(client):
    unique_username = f"testuser_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    payload = {
        "username": unique_username,
        "password": "securepassword123"
    }

    response = client.post("/api/auth/register", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "User created successfully"
    assert data["user"]["username"] == unique_username
    assert data["user"]["id"] is not None


def test_login_returns_token_for_valid_credentials(client):
    unique_username = f"user_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    password = "securepassword123"

    # User anlegen
    register_response = client.post(
        "/api/auth/register",
        json={"username": unique_username, "password": password},
    )
    assert register_response.status_code == 201

    # Login testen
    login_response = client.post(
        "/api/auth/login",
        json={"username": unique_username, "password": password},
    )
    data = login_response.get_json()

    assert login_response.status_code == 200
    assert "access_token" in data
    assert data["user"]["username"] == unique_username


def test_create_public_event_requires_auth(client):
    event_payload = {
        "title": "Public Test Event",
        "description": "Nur fuer den Test",
        "date": "2026-03-01T18:00:00Z",
        "location": "Berlin",
        "is_public": True,
    }

    response = client.post("/api/events", json=event_payload)

    assert response.status_code == 401


def test_create_public_event_succeeds_with_token(client):
    unique_username = f"user_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    password = "securepassword123"

    register_response = client.post(
        "/api/auth/register",
        json={"username": unique_username, "password": password},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={"username": unique_username, "password": password},
    )
    assert login_response.status_code == 200
    token = login_response.get_json()["access_token"]

    event_payload = {
        "title": "Public Test Event",
        "description": "Nur fuer den Test",
        "date": "2026-03-01T18:00:00Z",
        "location": "Berlin",
        "is_public": True,
    }

    response = client.post(
        "/api/events",
        json=event_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["title"] == "Public Test Event"
    assert data["is_public"] is True
    assert data["created_by"] is not None


def test_register_user_with_duplicate_username_fails(client):
    payload = {
        "username": "duplicate_user",
        "password": "securepassword123",
    }

    first_response = client.post("/api/auth/register", json=payload)
    second_response = client.post("/api/auth/register", json=payload)
    data = second_response.get_json()

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert data["error"] == "Username already exists"


def test_rsvp_to_non_public_event_requires_auth(client):
    username = "owner_nonpublic"
    password = "pw123456"
    client.post("/api/auth/register", json={"username": username, "password": password})
    login_resp = client.post("/api/auth/login", json={"username": username, "password": password})
    token = login_resp.get_json()["access_token"]

    event_payload = {
        "title": "Privates Event",
        "description": "Nur mit Auth",
        "date": "2026-03-01T18:00:00Z",
        "location": "München",
        "is_public": False
    }

    create_resp = client.post(
        "/api/events",
        json=event_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_resp.status_code == 201
    event_id = create_resp.get_json()["id"]

    rsvp_resp = client.post(f"/api/rsvps/event/{event_id}", json={"attending": True})
    assert rsvp_resp.status_code == 401
    assert rsvp_resp.get_json().get("error") == "Authentication required for this event"