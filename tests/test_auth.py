#----------------------------------
#  SIGNUP Tests
# ------------------------------

def test_signup_ok (client):
    response = client.post(
        "/auth/signup",
        json={
            "username": "Test",
            "password": "secret"
        }
    )
    assert response.status_code ==201
    data = response.json()
    assert data["username"] == "Test"
    assert "id" in data
    assert "password" not in data

def test_signup_username_already_taken(client):
    first_signup = client.post(
        "/auth/signup",
        json={
            "username": "Test",
            "password": "secret"
        })
    response = client.post(
        "/auth/signup",
        json={
            "username": "Test",
            "password": "secret"
        })
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already taken"

#-------------------------------------------
# Log in Test
# ---------------------------------------
def test_log_in_ok(client):
    client.post("/auth/signup",
                json = {
                    "username": "TestLogIn",
                    "password": "secret"
                })
    response = client.post(
        "auth/login",
        json={
            "username": "TestLogIn",
            "password": "secret"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data

def test_login_wrong_password(client):
    client.post("/auth/signup",
                json={
                    "username": "TestLogIn",
                    "password": "secret"
                })
    response = client.post(
        "auth/login",
        json={
            "username": "TestLogIn",
            "password": "secreterror"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid username or password"

def test_login_user_not_found(client):
    response = client.post(
        "auth/login",
        json={
            "username": "TestUsernameInexistant",
            "password": "secreterror"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid username or password"

#--------------
# Test protected END
#------------------
def test_protect_endpoint_without_token(client):
    response = client.get(
        "/games")

    assert response.status_code == 401

def test_protect_endpoint_invalid_token(client):
    response = client.get(
        "/games",
        headers ={"Authorization": "Bearer totally.invalid.token"})

    assert response.status_code == 401