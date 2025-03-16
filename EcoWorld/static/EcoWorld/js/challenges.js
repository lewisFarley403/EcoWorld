document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".complete-btn").forEach(button => {
        button.addEventListener("click", function () {
            const url = this.dataset.url;
            if (url) {
                window.location.href = url; // Redirect to challenge page
            }
        });
    });
});


// Function to mark a challenge as completed
function completeChallenge(challengeId, button) {
    fetch("/ecoworld/complete_challenge/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ id: challengeId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const challengeCard = button.closest(".challenge-card");
            challengeCard.classList.add("fade-out");
            setTimeout(() => {
                challengeCard.remove();
                fetchNewChallenge();
            }, 500);

            // Update Progress Tracker dynamically
            const progressElement = document.querySelector(".progress-tracker-section progress:first-of-type");
            const progressCount = progressElement.nextElementSibling;

            let currentValue = parseInt(progressElement.value);
            let maxValue = parseInt(progressElement.max);
            let newValue = currentValue + 1;

            updateProgressBar(progressElement, newValue, maxValue);
            progressCount.textContent = `${newValue}/${maxValue}`;
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error completing challenge:", error));
}

// Function to fetch a new challenge when one is completed
function fetchNewChallenge() {
    fetch("/ecoworld/get_next_challenge/")
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const newChallenge = data.challenge;
            const challengeContainer = document.getElementById("challenges-container");

            // Create a new challenge card dynamically
            const newCard = document.createElement("div");
            newCard.classList.add("challenge-card");
            newCard.innerHTML = `
                <span class="challenge-title">${newChallenge.name}</span>
                <button class="complete-btn" data-challenge-id="${newChallenge.id}" onclick="completeChallenge('${newChallenge.id}', this)">✔</button>
            `;

            challengeContainer.appendChild(newCard);
        }
    })
    .catch(error => console.error("Error fetching new challenge:", error));
}

function incrementObjective(objectiveId, button) {
    fetch("/ecoworld/increment_objective/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ objective_id: objectiveId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let progressSpan = button.nextElementSibling;
            let parts = progressSpan.textContent.split("/");
            let total = parseInt(parts[1]);
            let newProgress = data.progress;

            progressSpan.textContent = `${newProgress}/${total}`;

            const progressElement = document.querySelector(".progress-tracker-section .progress-item:nth-of-type(2) progress");
            const progressCount = progressElement.nextElementSibling;

            let currentValue = parseInt(progressElement.value);
            let maxValue = parseInt(progressElement.max);
            let newValue = data.completed_objectives;  // Now correctly fetched from backend

            updateProgressBar(progressElement, newValue, maxValue);
            progressCount.textContent = `${newValue}/${maxValue}`;

            if (newProgress === total) {
                let userResponse = prompt("Great job! Describe what you did:");
                if (userResponse) {
                    fetch("/ecoworld/save_objective_note/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCSRFToken(),
                        },
                        body: JSON.stringify({
                            objective_id: objectiveId,
                            message: userResponse,
                        }),
                    })
                    .catch(error => console.error("Error saving objective note:", error));
                }
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error("Error incrementing objective:", error));
}




// Function to update progress bar dynamically
function updateProgressBar(progressElement, newValue, maxValue) {
    const initialValue = parseInt(progressElement.value);
    const step = (newValue - initialValue) / 20; // Smooth animation steps
    let current = initialValue;

    const animate = setInterval(() => {
        current += step;
        if ((step > 0 && current >= newValue) || (step < 0 && current <= newValue)) {
            progressElement.value = newValue;
            clearInterval(animate);
        } else {
            progressElement.value = current;
        }
    }, 25);
}

// Helper function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}
// Auto-refresh daily objectives and challenges every X milliseconds
const RESET_INTERVAL = 10000;  // Must match Python interval




