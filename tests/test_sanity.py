def test_app_is_running(client):
    response = client.get("/")
    assert response.status_code == 200