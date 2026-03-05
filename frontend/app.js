// ==========================
// CONFIG
// ==========================

const API_URL = "https://web-production-75841.up.railway.app";

let authToken = null;
let currentGameId = null;
let selectedColor = null;
let currentGuess = [null, null, null, null];
let currentRowIndex = 0;


// ==========================
// BEST SCORE
// ==========================

let bestScore = localStorage.getItem("bestScore") || 0;
document.getElementById("best-score-value").textContent = bestScore;

async function fetchBestScore() {

  try {

    const response = await fetch(`${API_URL}/user/best-score`, {
      headers: {
        Authorization: `Bearer ${authToken}`
      }
    });

    if (!response.ok) return;

    const data = await response.json();

    document.getElementById("best-score-value").textContent = data.best_score;

  } catch (error) {

    console.log("Best score unavailable");

  }

}


// ==========================
// DIFFICULTY CONFIG
// ==========================

const difficultyConfig = {

  easy: {
    rows: 12,
    colors: ["red", "yellow", "blue", "green"]
  },

  medium: {
    rows: 10,
    colors: ["red", "yellow", "blue", "green", "white", "black"]
  },

  hard: {
    rows: 8,
    colors: ["red", "yellow", "blue", "green", "black", "white", "orange", "purple"]
  }

};

const difficultyMap = {
  1: "easy",
  2: "medium",
  3: "hard"
};


// ==========================
// AUTH LOGIN
// ==========================

loginForm.addEventListener("submit", async (e) => {

  e.preventDefault();

  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const response = await fetch(`${API_URL}/auth/login`, {

    method: "POST",

    headers: {
      "Content-Type": "application/json"
    },

    body: JSON.stringify({
      username,
      password
    })

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

});


// ==========================
// START GAME
// ==========================

document.getElementById("start-game-btn").addEventListener("click", async () => {

  const difficulty = difficultyMap[difficultyRange.value];

  try {

    const response = await fetch(`${API_URL}/game/create`, {

      method: "POST",

      headers: {

        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`

      },

      body: JSON.stringify({
        difficulty
      })

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

  }

  catch (error) {

    alert("Connection error");

  }

});


// ==========================
// SUBMIT GUESS
// ==========================

document.getElementById("submit-guess-btn").addEventListener("click", async () => {

  if (currentGuess.includes(null)) {

    alert("Fill all slots");
    return;

  }

  try {

    const response = await fetch(`${API_URL}/game/${currentGameId}/move`, {

      method: "POST",

      headers: {

        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`

      },

      body: JSON.stringify({

        guess: currentGuess.join(",")

      })

    });

    if (!response.ok) {

      alert("Move error");
      return;

    }

    const result = await response.json();

    updateBoard(result);

    handleGameStatus(result);

    resetGuess();

  }

  catch (error) {

    alert("Connection error");

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

  currentRowIndex++;

}


// ==========================
// GAME STATUS
// ==========================

function handleGameStatus(result) {

  if (result.status === "won") {

    alert(`🎉 You won! Score: ${result.score}`);

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


// ==========================
// RESET GUESS
// ==========================

function resetGuess() {

  currentGuess = [null, null, null, null];

  selectedColor = null;

  document.querySelectorAll(".color-btn").forEach(btn => {

    btn.style.outline = "none";

  });

}