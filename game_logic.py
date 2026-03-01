import random

# Rules of the game
#‘’'Guess a secret combination of colors in a limited number of attempts.
#Clues will help you progress.
#Clues:
#Black token = You have placed a token with the correct color in the correct position.
#Gray token = You have placed a token with the correct color, but not in the correct position.

colors= ['red', 'yellow', 'blue', 'green', 'black', 'white', 'orange', 'purple']

# Configuration des difficultés (nombre de couleurs disponibles)
DIFFICULTY_COLORS = {
    "easy": 4,  # red, yellow, blue, green
    "medium": 6,  # + white, black
    "hard": 8,  # + orange, purple

}
DIFFICULTY_MAX_TURNS = {
    "easy": 12,
    "medium": 10,
    "hard": 8
}


def generate_solution(difficulty: str) -> str:
    # Nombre de couleurs selon la difficulté
    num_colors = DIFFICULTY_COLORS[difficulty]
    available_colors = colors[:num_colors]  # Prend les N premières couleurs

    # Toujours 4 positions à deviner
    length = 4

    pegs_to_find = []
    for i in range(length):
        peg = random.choice(available_colors)
        pegs_to_find.append(peg)

    return ",".join(pegs_to_find)

def check_guess(solution: str, guess: str) -> tuple[int, int]:
    solution_list = [c.strip() for c in solution.split(",")]
    guess_list = [c.strip() for c in guess.split(",")]

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


def calculate_score(difficulty: str, turn_number: int) -> int:
    """Calculates the final score of a game won."""

    multiplicator = {
        "easy": 1,
        "medium": 2,
        "hard": 3
    }

    max_turns = DIFFICULTY_MAX_TURNS[difficulty]

    score = (max_turns - turn_number + 1) * 10 * multiplicator[difficulty]
    return int(score)

