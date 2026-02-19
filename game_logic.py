import random

# Rules of the game
#‘’'Guess a secret combination of colors in a limited number of attempts.
#Clues will help you progress.
#Clues:
#Black token = You have placed a token with the correct color in the correct position.
#Gray token = You have placed a token with the correct color, but not in the correct position.

colors= ['red', 'yellow', 'blue', 'green', 'black', 'white', 'orange', 'purple']

#Computer picks x pegs
def generate_solution(difficulty: str) -> str:
    lengths = {
        "easy": 4,
        "medium": 4,
        "hard": 5,
        "evil": 6
    }
    length = lengths[difficulty]

    pegs_to_find = []
    for i in range(length):
        peg = random.choice(colors)
        pegs_to_find.append(peg)
    return ",".join(pegs_to_find)

def check_guess(solution: str, guess: str) -> tuple[int, int]:
    solution_list = solution.split(",")
    guess_list = guess.split(",")

    black_tokens = 0
    white_tokens = 0

    index_solution_used = set()
    index_guess_used = set()

    # Black token
    for i in range(len(solution_list)):
        if solution_list[i] == guess_list[i]:
            index_guess_used.add(i)
            index_solution_used.add(i)
            black_tokens += 1
    # White token
    for i in range(len(solution_list)):
        if i in index_guess_used:
            continue
        for j in range(len(solution_list)):
            if j in index_solution_used:
                continue
            if guess_list[i]== solution_list[j]:
                white_tokens += 1
                index_guess_used.add(i)
                index_solution_used.add(j)
                break
    return black_tokens, white_tokens


def is_game_won(solution: str, guess: str) -> bool:
    """Vérifie si le joueur a gagné."""
    black_tokens, white_tokens = check_guess(solution, guess)

    # Gagné si tous les tokens sont noirs
    if black_tokens == len(solution.split(",")):
        return True
    else:
        return False


def calculate_score(difficulty: str, turn_number: int, max_turns: int = 12) -> int:
    """Calculates the final score of a game won."""
    multiplicator = {
        "easy": 1,
        "medium": 1.5,
        "hard": 2,
        "evil": 3
    }

    score = (max_turns - turn_number)*10*multiplicator[difficulty]
    return int(score)

