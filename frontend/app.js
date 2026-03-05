// ==========================
// CONFIG
// ==========================

const API_URL = 'https://web-production-75841.up.railway.app';

let authToken = null;
let currentGameId = null;
let selectedColor = null;
let currentGuess = [null, null, null, null];
let currentRowIndex = 0;

// ==========================
// Best score
// ==========================

let bestScore = localStorage.getItem("bestScore") || 0;
document.getElementById("best-score-value").textContent = bestScore;

async function fetchBestScore() {

    try {

        const response = await fetch(
            API_URL + "/user/best-score",
            {
                headers: {
                    'Authorization': 'Bearer ' + authToken
                }
            }
        );

        if (!response.ok) return;

        const data = await response.json();

        document.getElementById("best-score-value").textContent = data.best_score;

    } catch (error) {
        console.log("Error fetching best score");
    }
}

// ==========================
// DIFFICULTY CONFIG
// ==========================

const difficultyConfig = {
    easy: {
        rows: 12,
        colors: ["red", "yellow", "blue", "green" ]
    },
    medium: {
        rows: 10,
        colors: ["red", "yellow", "blue", "green" ,"white",  "black"]
    },
    hard: {
        rows: 8,
        colors: ["red", "yellow", "blue", "green" , "black", "white", "orange", "purple"]
    }
};

const difficultyMap = {
    1: "easy",
    2: "medium",
    3: "hard"
};


// ==========================
// DOM
// ==========================

const authSection = document.getElementById('auth-section');
const gameSection = document.getElementById('game-section');
const playSection = document.getElementById('play-section');

const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const signupText = document.getElementById("signup-text");
const loginText = document.getElementById("login-text");

const difficultyModal = document.getElementById('difficulty-modal');
const difficultyRange = document.getElementById('difficulty-range');
const difficultyLabel = document.getElementById('difficulty-label');
const authTitle = document.getElementById("auth-title");
const logoutBtn = document.getElementById("logout-btn");

// ==========================
// AUTH FUNCTIONS
// ==========================

function switchToLogin() {
    signupForm.style.display = "none";
    loginForm.style.display = "block";

    signupText.style.display = "block";
    loginText.style.display = "none";

    authTitle.textContent = "Log in";
}

function switchToSignup() {
    loginForm.style.display = "none";
    signupForm.style.display = "block";

    signupText.style.display = "none";
    loginText.style.display = "block";

    authTitle.textContent = "Create an account";
}


// ==========================
// AUTH SWITCH EVENTS
// ==========================

document.getElementById("show-signup-link").addEventListener("click", (e) => {
    e.preventDefault();
    switchToSignup();
});

document.getElementById("show-login-link").addEventListener("click", (e) => {
    e.preventDefault();
    switchToLogin();
});


// ==========================
// AUTH LOGIN
// ==========================

loginForm.addEventListener('submit', async (e) => {

    e.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {

        const response = await fetch(API_URL + '/auth/login', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            alert("Invalid credentials");
            return;
        }

        const data = await response.json();
        authToken = data.access_token;

        authSection.style.display = "none";
        gameSection.style.display = "block";
        document.getElementById("username-display").textContent = username;
        fetchBestScore();
    } catch (error) {
        alert("Connection error: " + error);
    }
});


// ==========================
// AUTH SIGNUP
// ==========================

signupForm.addEventListener('submit', async (e) => {

    e.preventDefault();

    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

    try {

        const response = await fetch(API_URL + '/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            alert("Signup failed");
            return;
        }

        alert("Account created successfully! You can now log in.");

        signupForm.reset();
        switchToLogin();

    } catch (error) {
        alert("Connection error: " + error);
    }
});

// ==========================
// LOGOUT
// ==========================

logoutBtn.addEventListener("click", () => {

    // Supprimer le token
    authToken = null;

    // Reset jeu
    currentGameId = null;
    currentRowIndex = 0;
    currentGuess = [null, null, null, null];
    selectedColor = null;

    // Reset UI
    document.getElementById("board").innerHTML = "";
    document.getElementById("color-palette").innerHTML = "";

    playSection.style.display = "none";
    gameSection.style.display = "none";
    authSection.style.display = "block";

    switchToLogin(); // revenir sur login
});

// ==========================
// OPEN / CLOSE MODAL
// ==========================

document.addEventListener("DOMContentLoaded", () => {

    const createGameBtn = document.getElementById("create-game-btn");
    const cancelGameBtn = document.getElementById("cancel-game-btn");
    const playAgainBtn = document.getElementById("play-again");

    // OPEN MODAL (Start a game)
    if (createGameBtn) {
        createGameBtn.addEventListener("click", () => {
            difficultyModal.style.display = "flex";
        });
    }

    // CLOSE MODAL
    if (cancelGameBtn) {
        cancelGameBtn.addEventListener("click", () => {
            difficultyModal.style.display = "none";
        });
    }

    // PLAY AGAIN
    if (playAgainBtn) {
        playAgainBtn.addEventListener("click", () => {

            // Reset variables
            currentGameId = null;
            currentRowIndex = 0;
            currentGuess = [null, null, null, null];
            selectedColor = null;

            // Reset UI
            document.getElementById("board").innerHTML = "";
            document.getElementById("color-palette").innerHTML = "";

            document.getElementById("submit-guess-btn").disabled = false; //

            // Cacher la section de jeu
            playSection.style.display = "none";

            // Ouvrir la modal de difficulté
            difficultyModal.style.display = "flex";
        });
    }

});


// ==========================
// SLIDER LABEL
// ==========================

difficultyRange.addEventListener('input', (e) => {

    const labels = {
        1: "Easy",
        2: "Medium",
        3: "Hard"
    };

    difficultyLabel.textContent = labels[e.target.value];
});


// ==========================
// START GAME
// ==========================

document.getElementById('start-game-btn').addEventListener('click', async () => {

    const difficulty = difficultyMap[difficultyRange.value];

    try {

        const response = await fetch(API_URL + '/game/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + authToken
            },
            body: JSON.stringify({ difficulty })
        });

        if (!response.ok) {
            alert("Error creating game");
            return;
        }

        const game = await response.json();
        currentGameId = game.id;

        generateBoard(difficultyConfig[difficulty].rows);
        renderColorPalette(difficulty);

        currentRowIndex = 0;

        difficultyModal.style.display = "none";
        gameSection.style.display = "none";
        playSection.style.display = "block";

        resetGuess();

    } catch (error) {
        alert("Connection error: " + error);
    }
});


// ==========================
// GENERATE BOARD
// ==========================

function generateBoard(rows) {

    const board = document.getElementById("board");
    board.innerHTML = "";

    for (let i = 0; i < rows; i++) {

        const row = document.createElement("div");
        row.classList.add("game-row");

        for (let j = 0; j < 4; j++) {
            const slot = document.createElement("div");
            slot.classList.add("slot");
            slot.dataset.index = j;
            row.appendChild(slot);
        }

        const feedback = document.createElement("div");
        feedback.classList.add("feedback");
        row.appendChild(feedback);

        board.appendChild(row);
    }
}


// ==========================
// GENERATE PALETTE
// ==========================

function renderColorPalette(difficulty) {

    const palette = document.getElementById("color-palette");
    palette.innerHTML = "";

    difficultyConfig[difficulty].colors.forEach(color => {

        const btn = document.createElement("div");
        btn.classList.add("color-btn");
        btn.style.backgroundColor = color;
        btn.dataset.color = color;

        btn.addEventListener("click", () => {

            selectedColor = color;

            document.querySelectorAll(".color-btn").forEach(b => {
                b.style.outline = "none";
            });

            btn.style.outline = "3px solid white";
        });

        palette.appendChild(btn);
    });
}


// ==========================
// SLOT CLICK
// ==========================

document.getElementById("board").addEventListener("click", (e) => {

    const slot = e.target;
    if (!slot.classList.contains("slot")) return;
    if (!selectedColor) return;

    const rows = document.querySelectorAll(".game-row");
    const row = slot.parentElement;
    const rowIndex = Array.from(rows).indexOf(row);

    if (rowIndex !== currentRowIndex) return;

    const index = slot.dataset.index;
    slot.style.backgroundColor = selectedColor;
    currentGuess[index] = selectedColor;
});


// ==========================
// SUBMIT GUESS
// ==========================

document.getElementById('submit-guess-btn').addEventListener('click', async () => {

    if (currentGuess.includes(null)) {
        alert("Fill all 4 slots!");
        return;
    }

    try {

        const response = await fetch(
            API_URL + `/game/${currentGameId}/move`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + authToken
                },
                body: JSON.stringify({
                    guess: currentGuess.join(",")
                })
            }
        );

        if (!response.ok) {
            alert("Error submitting move");
            return;
        }

        const result = await response.json();
        console.log(result);

        handleGameStatus(result);
        updateBoard(result);
        resetGuess();

    } catch (error) {
        alert("Connection error: " + error);
    }
});


// ==========================
// UPDATE BOARD
// ==========================

function updateBoard(move) {

    const rows = document.querySelectorAll(".game-row");
    if (currentRowIndex >= rows.length) return;

    const row = rows[currentRowIndex];
    const guessArray = move.guess.split(",");
    const slots = row.querySelectorAll(".slot");

    guessArray.forEach((color, index) => {
        slots[index].style.backgroundColor = color;
    });

    const feedback = row.querySelector(".feedback");
    feedback.innerHTML = "";

    const fragment = document.createDocumentFragment();

// Noir
for (let i = 0; i < move.correct_positions; i++) {
    const peg = document.createElement("div");
    peg.classList.add("correct");
    fragment.appendChild(peg);
}

// Blanc
for (let i = 0; i < move.wrong_positions; i++) {
    const peg = document.createElement("div");
    peg.classList.add("misplaced");
    fragment.appendChild(peg);
}

feedback.innerHTML = "";
feedback.appendChild(fragment);

    currentRowIndex++;
}

function handleGameStatus(result) {

    if (result.status === "won") {

        alert(`🎉 You won! Your score: ${result.score} points`);

        if (result.score > bestScore) {
            bestScore = result.score;
            localStorage.setItem("bestScore", bestScore);
            document.getElementById("best-score-value").textContent = bestScore;
        }
    }

    if (result.status === "lost") {

        alert("💀 You lost!");

        if (result.solution) {
            showSolution(result.solution);
        }

        document.getElementById("submit-guess-btn").disabled = true;
    }
}


function showSolution(solution) {

    const board = document.getElementById("board");

    const solutionRow = document.createElement("div");
    solutionRow.classList.add("game-row");

    const colors = solution.split(",");

    colors.forEach(color => {
        const slot = document.createElement("div");
        slot.classList.add("slot");
        slot.style.backgroundColor = color;
        solutionRow.appendChild(slot);
    });

    const label = document.createElement("div");
    label.textContent = " ← Solution";
    label.style.marginLeft = "10px";
    label.style.color = "white";

    solutionRow.appendChild(label);

    board.appendChild(solutionRow);
}

// ==========================
// RESET
// ==========================

function resetGuess() {
    currentGuess = [null, null, null, null];
    selectedColor = null;

    document.querySelectorAll(".color-btn").forEach(btn => {
        btn.style.outline = "none";
    });
}
// ==========================
// Ask for rules
// ==========================

const rulesbtn = document.getElementById("rules-btn");

if (rulesbtn) {
    rulesbtn.addEventListener("click", () => {
        alert(`MASTER MIND RULES

You have to find the secret code using the available colors.
• Colors can be repeated.
• After each guess you get feedback:
   ⚫ Black peg = correct color AND correct position
   ⚪ White peg = correct color but wrong position
• You win if you find the secret code.
• You lose if you run out of attempts.

Good luck!`);
    });
}
