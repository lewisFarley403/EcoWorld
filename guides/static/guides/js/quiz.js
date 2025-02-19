console.log('javascript loaded')
document.addEventListener("DOMContentLoaded", function() {
    let currentQuestion = 0;
    const questions = [
        {
            question: "Which of the following actions can help reduce energy consumption at home? (Select all that apply)",
            answers: [
                { text: "Using incandescent lightbulbs", value: "A", correct: false },
                { text: "Unplugging devices when not in use", value: "B", correct: true },
                { text: "Using a programmable thermostat", value: "C", correct: true },
                { text: "Keeping lights on during the day", value: "D", correct: false }
            ]
        },
        {
            question: "What are some ways to minimize water waste? (Select all that apply)",
            answers: [
                { text: "Fixing leaky faucets", value: "A", correct: true },
                { text: "Running half-loads of laundry", value: "B", correct: false },
                { text: "Installing low-flow showerheads", value: "C", correct: true },
                { text: "Collecting rainwater for gardening", value: "D", correct: true }
            ]
        },
        {
            question: "Which of the following are part of the '3 Rs' of sustainability? (Select all that apply)",
            answers: [
                { text: "Reduce", value: "A", correct: true },
                { text: "Reuse", value: "B", correct: true },
                { text: "Recycle", value: "C", correct: true },
                { text: "Replace", value: "D", correct: false }
            ]
        },
        {
            question: "Which of the following transportation methods has the lowest environmental impact? (Select all that apply)",
            answers: [
                { text: "Driving alone in a gas-powered car", value: "A", correct: false },
                { text: "Taking a train", value: "B", correct: true },
                { text: "Flying short distances", value: "C", correct: false },
                { text: "Biking or walking", value: "D", correct: true }
            ]
        },
        {
            question: "What are some sustainable shopping practices? (Select all that apply)",
            answers: [
                { text: "Buying locally produced goods", value: "A", correct: true },
                { text: "Choosing products with minimal packaging", value: "B", correct: true },
                { text: "Purchasing second-hand items", value: "C", correct: true },
                { text: "Always buying new products", value: "D", correct: false }
            ]
        },
        {
            question: "How can your diet help reduce your environmental footprint? (Select all that apply)",
            answers: [
                { text: "Eating more plant-based meals", value: "A", correct: true },
                { text: "Choosing sustainably sourced seafood", value: "B", correct: true },
                { text: "Reducing meat and dairy consumption", value: "C", correct: true },
                { text: "Wasting more food", value: "D", correct: false }
            ]
        }
    ];

    // Shuffle the questions array
    questions.sort(() => Math.random() - 0.5);

    const totalQuestions = questions.length;
    const nextButton = document.getElementById("next-button");
    const backButton = document.getElementById("back-button");
    const submitButton = document.getElementById("submit-button");
    const progressBar = document.getElementById("progress-bar");
    const questionsContainer = document.getElementById("questions-container");

    // Store the selected answers
    let selectedAnswers = {};

    // Function to generate the questions dynamically
    function generateQuestions() {
        questions.forEach((q, index) => {
            const questionBox = document.createElement("div");
            questionBox.classList.add("question-box");
            questionBox.id = `question-${index + 1}`;

            const questionText = document.createElement("div");
            questionText.classList.add("question-text");
            questionText.textContent = q.question;
            questionBox.appendChild(questionText);

            q.answers.forEach((answer) => {
                const answerBox = document.createElement("div");
                answerBox.classList.add("answer-box");
                answerBox.setAttribute("data-question", `q${index + 1}`);
                answerBox.setAttribute("data-value", answer.value);
                answerBox.textContent = answer.text;
                questionBox.appendChild(answerBox);
            });

            questionsContainer.appendChild(questionBox);
        });
    }

    // Function to navigate to the next question
    function showQuestion(questionNumber, direction) {
        const allQuestions = document.querySelectorAll(".question-box");
        allQuestions.forEach((question) => {
            question.classList.remove("active", "slide-in-next", "slide-out-next", "slide-in-prev", "slide-out-prev");
        });

        const currentQuestionBox = document.getElementById(`question-${questionNumber + 1}`);
        if (currentQuestionBox) {
            if (direction === "next") {
                currentQuestionBox.classList.add("active", "slide-in-next");
            } else if (direction === "prev") {
                currentQuestionBox.classList.add("active", "slide-in-prev");
            }
        }

        // Handle button visibility
        if (currentQuestion === 0) {
            backButton.style.display = "none";
        } else {
            backButton.style.display = "inline-block";
        }

        if (currentQuestion === totalQuestions - 1) {
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
        const progress = ((currentQuestion + 1) / totalQuestions) * 100;
        progressBar.style.width = `${progress}%`;
    }

    // Generate questions and show the first question
    generateQuestions();
    showQuestion(currentQuestion, "next");

    // Event listener for the Next button
    nextButton.addEventListener("click", function() {
        if (currentQuestion < totalQuestions - 1) {
            nextButton.disabled = true;
            const currentQuestionBox = document.getElementById(`question-${currentQuestion + 1}`);
            currentQuestionBox.classList.add("slide-out-next");
            setTimeout(() => {
                currentQuestion++;
                showQuestion(currentQuestion, "next");
                nextButton.disabled = false;
            }, 500); // Wait for the slide-out to complete
        }
    });

    // Event listener for the Back button
    backButton.addEventListener("click", function() {
        if (currentQuestion > 0) {
            backButton.disabled = true;
            const currentQuestionBox = document.getElementById(`question-${currentQuestion + 1}`);
            currentQuestionBox.classList.add("slide-out-prev");
            setTimeout(() => {
                currentQuestion--;
                showQuestion(currentQuestion, "prev");
                backButton.disabled = false;
            }, 500); // Wait for the slide-out to complete
        }
    });

    // Event listener for the Submit button
    submitButton.addEventListener("click", function() {
        let score = 0;
        const correctAnswers = {};

        // Generate correct answers object
        questions.forEach((q, index) => {
            correctAnswers[`q${index + 1}`] = new Set(q.answers.filter(a => a.correct).map(a => a.value));
        });

        // Calculate score
        for (let question in correctAnswers) {
            if (selectedAnswers[question] &&
                correctAnswers[question].size === selectedAnswers[question].size &&
                [...correctAnswers[question]].every((ans) => selectedAnswers[question].has(ans))) {
                score++;
            }
        }
        console.log(score);
        alert("Your score: " + score + "/" + totalQuestions);

        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
        console.log(csrfToken)
        fetch('/guides/registerScore/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({score:score})
        })
    });

    // Store the selected answers when users click on answer boxes
    questionsContainer.addEventListener("click", function(event) {
        if (event.target.classList.contains("answer-box")) {
            const question = event.target.getAttribute("data-question");
            const value = event.target.getAttribute("data-value");

            if (!selectedAnswers[question]) {
                selectedAnswers[question] = new Set();
            }

            if (selectedAnswers[question].has(value)) {
                selectedAnswers[question].delete(value);
                event.target.classList.remove("selected");
            } else {
                selectedAnswers[question].add(value);
                event.target.classList.add("selected");
            }
        }
    });
});