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

            // Fade out the completed challenge
            challengeCard.classList.add("fade-out");
            setTimeout(() => {
                challengeCard.remove(); // Remove challenge after animation
                fetchNewChallenge(); // Fetch the next available challenge
            }, 500);
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
    const API_ENDPOINTS = {
        incrementObjective: "/ecoworld/increment_objective/",
        saveObjectiveNote: "/ecoworld/save_objective_note/",
    };

    const MESSAGES = {
        taskComplete: "Great job! Describe what you did:",
    };

    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        console.error("CSRF token not found. Request aborted.");
        alert("An error occurred. Please refresh the page and try again.");
        return;
    }

    fetch(API_ENDPOINTS.incrementObjective, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ objective_id: objectiveId }),
    })
    .then(response => response.json())
    .then(data => {
        progress = data.progress;
        if (data.success) {
            if (button && button.nextElementSibling) {
                let progressSpan = button.nextElementSibling;
                if (progressSpan.textContent.includes("/")) {
                    let parts = progressSpan.textContent.split("/");
                    let total = parts[1];
                    progressSpan.textContent = `${data.progress}/${total}`;

                    if (Number(data.progress) === Number(data.goal)) {
                        let userResponse = prompt("Great job! Describe what you did:");
                        if (userResponse) {
                            fetch("/ecoworld/save_objective_note/", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                    "X-CSRFToken": csrfToken,
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
                    console.error("Invalid progress span content");
                }
            } else {
                console.error("Button or progress span not found");
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error incrementing objective:", error);
        alert("There was an error processing your request. Please try again.");
    });
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

setInterval(() => {
    location.reload();
}, RESET_INTERVAL);



