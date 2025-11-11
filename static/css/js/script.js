// ===== DIFFICULTY SETTINGS =====
(function initDifficulty() {
    // Get difficulty from storage
    const difficulty = parseInt(
        sessionStorage.getItem("quizDifficulty") || 
        localStorage.getItem("quizDifficulty") || 
        1
    );
    
    // Apply settings
    switch(difficulty) {
        case 1: 
            window.quizSettings = { health: 15, length: 5 };
            playDifficultyMusic('easy-song');
            changeSprite('easySprite');
            break;
        case 2: 
            window.quizSettings = { health: 30, length: 10 };
            playDifficultyMusic('normal-song');
            changeSprite('normalSprite');
            break;
        case 3: 
            window.quizSettings = { health: 45, length: 15 };
            playDifficultyMusic('hard-song');
            changeSprite('hardSprite');
            break;
        default: 
            window.quizSettings = { health: 15, length: 5 };
            playDifficultyMusic('easy-song');
    }
    
    console.log("Difficulty initialized:", difficulty, window.quizSettings);
})();

// New function to handle music playback
function playDifficultyMusic(id) {
    // Wait for DOM to be fully ready
    document.addEventListener('DOMContentLoaded', () => {
        const audio = document.getElementById(id);
        if (!audio) {
            console.error("Audio element not found:", id);
            return;
        }
    });
} 

function changeSprite(id) {
    // Wait for DOM to be fully ready
    document.addEventListener('DOMContentLoaded', () => {
        const sprite = document.getElementById(id);
        if (!sprite) {
            console.error("Sprite element not found:", id);
            return;
        }
        sprite.style.display ="";
    });
} 

var health = window.quizSettings.health;
var quizLength = window.quizSettings.length;
var currentQuestion = 0;
var correctAnswer;
var correctResponses = 0;
var maxHealth = window.quizSettings.health;
var health = maxHealth;

document.addEventListener("DOMContentLoaded", function() {
    console.log("Quiz started with:", {
        difficulty: window.quizSettings.difficulty,
        health: health,
        length: quizLength
    });
    
    x = document.getElementById("hurt-sound");
    y = document.getElementById("correct-sound");
    table = document.getElementById("questionTable");
    
    // Initialize health display
    updateHealthDisplay();
    document.getElementById("quiz-progress").textContent = correctResponses + "/" + currentQuestion;
    
    if (table) replaceQuestion();
});

// New function to update health display
function updateHealthDisplay() {
    const healthBar = document.getElementById("health-bar");
    const healthText = document.getElementById("health-text");
    
    // Calculate percentage
    const healthPercentage = (health / maxHealth) * 100;
    
    // Update bar
    healthBar.style.width = `${healthPercentage}%`;
    
    // Update text (optional)
    healthText.textContent = `${health}/${maxHealth}`;
}

function bajarVida() {
    health -= 5;
    updateHealthDisplay();
    document.getElementById("quiz-progress").textContent = correctResponses + "/" + currentQuestion;
    
    if (health <= 0) endQuiz('game_over');
}

function replaceQuestion() {
    const tbody = table?.querySelector("tbody");
    if (!tbody || currentQuestion >= tbody.rows.length) {
        endQuiz('quiz_results');
        return;
    }
    
    const row = tbody.rows[currentQuestion];
    document.getElementById("question").textContent = row.cells[1].textContent;
    for (let i = 2; i <= 5; i++) {
        document.getElementById(`a${i-1}`).textContent = row.cells[i].textContent;
    }
    correctAnswer = parseInt(row.cells[6].textContent);
}

function answerQuestion(buttonId) {
    const isCorrect = parseInt(buttonId.replace("a", "")) === correctAnswer;
    
    if (isCorrect) {
        correctResponses++;
    } else {
        bajarVida();
    }
    
    currentQuestion++;
    document.getElementById("quiz-progress").textContent = correctResponses + "/" + currentQuestion;
    // Check quiz end conditions
    const maxQuestions = Math.min(
        table.getElementsByTagName("tbody")[0].rows.length,
        quizLength
    );
    
    if (currentQuestion >= maxQuestions) {
        endQuiz('quiz_results');
    } else {
        replaceQuestion();
    }
}

function endQuiz(resultsPage) {
    // Get quiz table from sessionStorage OR URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const quizTable = sessionStorage.getItem("quiz") || urlParams.get('quiz') || 'cuestionario_un';
    
    // Store results
    sessionStorage.setItem('quizResults', JSON.stringify({
        correct: correctResponses,
        total: quizLength,
        difficulty: sessionStorage.getItem("quizDifficulty") || 1,
        quizTable: quizTable
    }));
    
    // Redirect with parameters
    window.location.href = `${resultsPage}?quiz=${encodeURIComponent(quizTable)}&difficulty=${sessionStorage.getItem("quizDifficulty") || 1}`;
}