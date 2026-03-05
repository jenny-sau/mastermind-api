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
// DOM
// ==========================

const authSection = document.getElementById("auth-section");
const gameSection = document.getElementById("game-section");
const playSection = document.getElementById("play-section");

const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");

const difficultyModal = document.getElementById("difficulty-modal");
const difficultyRange = document.getElementById("difficulty-range");

const board = document.getElementById("board");
const palette = document.getElementById("color-palette");


// ==========================
// BEST SCORE
// ==========================

let bestScore = localStorage.getItem("bestScore") || 0;
document.getElementById("best-score-value").textContent = bestScore;

async function fetchBestScore() {

  try {

    const response = await fetch(`${API_URL}/user/best-score`, {
      headers: { Authorization: `Bearer ${authToken}` }
    });

    if (!response.ok) return;

    const data = await response.json();
    document.getElementById("best-score-value").textContent = data.best_score;

  } catch {
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
// LOGIN
// ==========================

loginForm.addEventListener("submit", async (e) => {

  e.preventDefault();

  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  const response = await fetch(`${API_URL}/auth/login`, {

    method: "POST",
    headers: { "Content-Type": "application/json" },
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

});


// ==========================
// START GAME
// ==========================

document.getElementById("start-game-btn").addEventListener("click", async () => {

  const difficulty = difficultyMap[difficultyRange.value];

  const response = await fetch(`${API_URL}/game/create`, {

    method: "POST",

    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${authToken}`
    },

    body: JSON.stringify({ difficulty })

  });

  if (!response.ok) {
    alert("Error creating game");
    return;
  }

  const game = await response.json();

  currentGameId = game.id;
  currentRowIndex = 0;

  generateBoard(difficultyConfig[difficulty].rows);
  renderColorPalette(difficulty);

  gameSection.style.display = "none";
  playSection.style.display = "block";

  resetGuess();

});


// ==========================
// GENERATE BOARD
// ==========================

function generateBoard(rows) {

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
// COLOR PALETTE
// ==========================

function renderColorPalette(difficulty) {

  palette.innerHTML = "";

  difficultyConfig[difficulty].colors.forEach(color => {

    const btn = document.createElement("div");

    btn.classList.add("color-btn");
    btn.style.backgroundColor = color;

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

board.addEventListener("click", (e) => {

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

document.getElementById("submit-guess-btn").addEventListener("click", async () => {

  if (currentGuess.includes(null)) {

    alert("Fill all slots");
    return;

  }

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

});


// ==========================
// UPDATE BOARD
// ==========================

function updateBoard(move) {

  const rows = document.querySelectorAll(".game-row");
  const row = rows[currentRowIndex];

  const guessArray = move.guess.split(",");
  const slots = row.querySelectorAll(".slot");

  guessArray.forEach((color, index) => {
    slots[index].style.backgroundColor = color;
  });

  const feedback = row.querySelector(".feedback");
  feedback.innerHTML = "";

  for (let i = 0; i < move.correct_positions; i++) {

    const peg = document.createElement("div");
    peg.classList.add("correct");

    feedback.appendChild(peg);

  }

  for (let i = 0; i < move.wrong_positions; i++) {

    const peg = document.createElement("div");
    peg.classList.add("misplaced");

    feedback.appendChild(peg);

  }

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

    document.getElementById("submit-guess-btn").disabled = true;

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
// SHOW SOLUTION
// ==========================

function showSolution(solution) {

  const solutionRow = document.createElement("div");
  solutionRow.classList.add("game-row");

  const colors = solution.split(",");

  colors.forEach(color => {

    const slot = document.createElement("div");
    slot.classList.add("slot");

    slot.style.backgroundColor = color;

    solutionRow.appendChild(slot);

  });

  board.appendChild(solutionRow);

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