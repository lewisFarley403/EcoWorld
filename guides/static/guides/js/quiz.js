document.addEventListener("DOMContentLoaded", function() {
    let currentQuestion = 1;
    const totalQuestions = 2; // Update this with the total number of questions ----------
    const nextButton = document.getElementById("next-button");
    const backButton = document.getElementById("back-button");
    const submitButton = document.getElementById("submit-button");
    const progressBar = document.getElementById("progress-bar");

    // Store the selected answers
    let selectedAnswers = {};

    // Function to navigate to the next question
    function showQuestion(questionNumber) {
        const allQuestions = document.querySelectorAll(".question-box");
        allQuestions.forEach((question) => {
            question.classList.remove("active", "slide-in", "slide-out");
        });

        const currentQuestionBox = document.getElementById(`question-${questionNumber}`);
        if (currentQuestionBox) {
            currentQuestionBox.classList.add("active", "slide-in");
        }

        // Handle button visibility
        if (currentQuestion === 1) {
            backButton.style.display = "none";
        } else {
            backButton.style.display = "inline-block";
        }

        if (currentQuestion === totalQuestions) {
            nextButton.style.display = "none";
            submitButton.style.display = "inline-block";
        } else {
            nextButton.style.display = "inline-block";
            submitButton.style.display = "none";
        }

        // Update progress bar
        updateProgressBar();
    }

    // Function to update the progress bar
    function updateProgressBar() {
        const progress = (currentQuestion / totalQuestions) * 100;
        progressBar.style.width = `${progress}%`;
    }

    // Show the first question
    showQuestion(currentQuestion);

    // Event listener for the Next button
    nextButton.addEventListener("click", function() {
        if (currentQuestion < totalQuestions) {
            currentQuestion++;
            const currentQuestionBox = document.getElementById(`question-${currentQuestion - 1}`);
            currentQuestionBox.classList.add("slide-out");
            setTimeout(() => {
                showQuestion(currentQuestion);
            }, 500); // Wait for the slide-out to complete
        }
    });

    // Event listener for the Back button
    backButton.addEventListener("click", function() {
        if (currentQuestion > 1) {
            currentQuestion--;
            const currentQuestionBox = document.getElementById(`question-${currentQuestion + 1}`);
            currentQuestionBox.classList.add("slide-out");
            setTimeout(() => {
                showQuestion(currentQuestion);
            }, 500); // Wait for the slide-out to complete
        }
    });

    // Event listener for the Submit button
    submitButton.addEventListener("click", function() {
        let score = 0;
        const correctAnswers = {
            q1: new Set(["B", "D"]), // Correct answers for question 1
            q2: new Set(["B", "D"]), // Correct answers for question 2
        };

        for (let question in correctAnswers) {
            if (selectedAnswers[question] &&
                correctAnswers[question].size === selectedAnswers[question].size &&
                [...correctAnswers[question]].every((ans) => selectedAnswers[question].has(ans))) {
                score++;
            }
        }

        alert("Your score: " + score + "/" + totalQuestions);
    });

    // Store the selected answers when users click on answer boxes
    const answerBoxes = document.querySelectorAll(".answer-box");
    answerBoxes.forEach((box) => {
        box.addEventListener("click", function() {
            const question = this.getAttribute("data-question");
            const value = this.getAttribute("data-value");

            if (!selectedAnswers[question]) {
                selectedAnswers[question] = new Set();
            }

            if (selectedAnswers[question].has(value)) {
                selectedAnswers[question].delete(value);
                this.classList.remove("selected");
            } else {
                selectedAnswers[question].add(value);
                this.classList.add("selected");
            }
        });
    });
});
