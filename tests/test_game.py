import pytest

#----------------
# Test: Create Game in easy + medium + hard level
# ------------------------------------------------
@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_create_game_ok(client, user_token, difficulty):
    response = client.post(
        "/game/create",
        json={"difficulty": difficulty},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["difficulty"] == difficulty

# -----------------------
# Test: Move
#------------------------
def test_play_move_ok(client, user_token, create_game):
    response = client.post(
        f"/game/{create_game}/move",
        json ={"guess": "red,blue,green,yellow"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["turn_number"] == 1
    assert "correct_positions" in data
    assert "wrong_positions" in data

def test_play_move_game_not_in_progress(client, user_token):
    response = client.post(
        f"/game/{1}/move",
        json={"guess": "red,blue,green,yellow"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found"


def test_play_move_game_non_existing(client, user_token):
    # create a game
    create_response = client.post(
        "/game/create",
        json={"difficulty": "easy"},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    game_id = create_response.json()["id"]
    solution = create_response.json()["solution"]

    # Win the game
    client.post(f"/game/{game_id}/move",
                json={"guess": solution},
                headers={"Authorization": f"Bearer {user_token}"}
                )

    # Try to play on game status = won
    response = client.post(f"/game/{game_id}/move",
                json= {"guess": "red,blue,green,yellow"},
                headers={"Authorization": f"Bearer {user_token}"})

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Game is already finished"


def test_play_move_not_mine(client, user_token, second_user_token):
    # first user create a game:
    first_create_response= client.post(
        "/game/create",
        json={"difficulty": "easy"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    game_id = first_create_response.json()["id"]

    # Second user try to play, on this game:
    response = client.post(f"/game/{game_id}/move",
                json={"guess": "red,blue,green,yellow"},
                headers={"Authorization": f"Bearer {second_user_token}"}
                )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found"

# ---------------------
# Get_game test
# ---------------------
def test_get_game_ok(client, user_token, create_game):
    response = client.get(
        f"/game/{create_game}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200

def test_get_game_non_existing_game (client, user_token):
    response = client.get(
        f"/game/{1}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Game not found"

def test_get_all_games_ok (client, user_token, create_game):
    response = client.get(
        "/games",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200