from game_logic import generate_solution, check_guess, is_game_won, calculate_score

def test_generate_solution_easy():
    solution = generate_solution("easy")
    colors_easy = ["red", "yellow", "blue", "green"]
    solution_list = solution.split(",")
    for color in solution_list:
        assert color in colors_easy
    assert len(solution_list) == 4

def test_generate_solution_medium():
    solution = generate_solution("medium")
    colors_easy = ["red", "yellow", "blue", "green", "white", "black"]
    solution_list = solution.split(",")
    for color in solution_list:
        assert color in colors_easy
    assert len(solution_list) == 4

def test_generate_solution_hard():
    solution = generate_solution("hard")
    colors_easy = ["red", "yellow", "blue", "green", "white", "black", "orange", "purple"]
    solution_list = solution.split(",")
    for color in solution_list:
        assert color in colors_easy
    assert len(solution_list) == 4

def test_check_guess():
    black_tokens, white_tokens= check_guess("red,blue,green,yellow", "blue,red,green,yellow")
    assert black_tokens == 2
    assert white_tokens == 2

    black_tokens, white_tokens = check_guess("red,blue,yellow,green", "green,red,blue,yellow")
    assert black_tokens == 0
    assert white_tokens == 4

    black_tokens, white_tokens = check_guess("red,red,red,red", "blue,blue,blue,blue")
    assert black_tokens == 0
    assert white_tokens == 0

    black_tokens, white_tokens = check_guess("red,blue,yellow,red", "red,blue,yellow,red")
    assert black_tokens == 4
    assert white_tokens == 0

def test_is_game_won():
    result = is_game_won("red,blue,green,yellow", "red,blue,green,yellow")
    assert result == True

    result = is_game_won("red,blue,green,yellow", "blue,blue,green,yellow")
    assert result == False

def test_calculate_score():
    result = calculate_score("easy", 1)
    assert result == 120

    result = calculate_score("medium", 1)
    assert result == 200

    result = calculate_score("hard", 1)
    assert result == 240

    result = calculate_score("easy", 4)
    assert result == 90

    result = calculate_score("medium", 4)
    assert result == 140

    result = calculate_score("hard", 4)
    assert result == 150

    result = calculate_score("easy", 12)
    assert result == 10

    result = calculate_score("medium", 10)
    assert result == 20

    result = calculate_score("hard", 8)
    assert result == 30