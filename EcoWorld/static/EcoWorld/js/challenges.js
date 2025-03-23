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

// Function to calculate total progress
function calculateTotalProgress() {
    // Calculate challenge progress
    const challengeCards = document.querySelectorAll('.challenge-card');
    const completedChallenges = document.querySelectorAll('.challenge-card.completed').length;
    
    // Calculate objective progress
    const allObjectiveCards = document.querySelectorAll('.objective-card');
    let totalTasks = 0;
    let completedTasks = 0;
    
    allObjectiveCards.forEach(card => {
        const progressText = card.querySelector('.progress-count').textContent;
        console.log("Progress text for card:", progressText);
        const [current, max] = progressText.split('/').map(num => parseInt(num.trim()));
        totalTasks += max;
        completedTasks += current;
    });

    console.log(`Total progress - Completed: ${completedTasks}, Total: ${totalTasks}`);
    return {
        // challenges: { completed: completedChallenges, total: challengeCards.length },
        objectives: { completed: completedTasks, total: totalTasks }
    };
}

// Function to update all progress bars
function updateAllProgress() {
    const progress = calculateTotalProgress();
    console.log("PROGRESS")
    console.log(progress.objectives.completed, progress.objectives.total)
    // Update challenges progress
    const challengeProgressElement = document.querySelector(".progress-tracker-section progress:first-of-type");
    const challengeProgressCount = challengeProgressElement.nextElementSibling;
    // updateProgressBar(challengeProgressElement, progress.challenges.completed, progress.challenges.total);
    // challengeProgressCount.textContent = `${progress.challenges.completed}/${progress.challenges.total}`;
    
    // Update objectives progress
    // const objectiveProgressElement = document.querySelector(".progress-tracker-section .progress-item:nth-of-type(2) progress");
    const objectiveProgressElement=document.getElementById("progress-bar")
    console.log(objectiveProgressElement)
    const objectiveProgressCount = objectiveProgressElement.nextElementSibling;
    updateProgressBar(objectiveProgressElement, progress.objectives.completed, progress.objectives.total);
    objectiveProgressCount.textContent = `${progress.objectives.completed}/${progress.objectives.total}`;
}

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
            const challengeCard = document.getElementById(`challenge-${challengeId}`);
            
            // Add completion class for styling
            challengeCard.classList.add("completed");
            
            // Disable the button
            const completeButton = challengeCard.querySelector(".complete-btn");
            completeButton.disabled = true;
            completeButton.textContent = "✓";
            completeButton.classList.add("completed-btn");
            
            // Update all progress bars
            updateAllProgress();
            
            // Refresh the page after a slight delay to allow animations to complete
            setTimeout(function() { 
                window.location.reload(); 
            }, 1500);
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
    console.log("Incrementing objective:", objectiveId);    
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
        console.log("Server response:", data);

        if (data.success) {
            // Find the objective card and its progress elements
            const objectiveCard = button.closest('.objective-card');
            const progressSpan = objectiveCard.querySelector('.progress-count');
            
            if (!progressSpan) {
                console.error("Progress span not found in:", objectiveCard);
                return;
            }

            let parts = progressSpan.textContent.split("/");
            let total = parseInt(parts[1]);
            let newProgress = data.progress;
            console.log(`Updating progress: ${newProgress}/${total}`);

            // Animate the progress text change
            progressSpan.style.transition = 'opacity 0.3s';
            progressSpan.style.opacity = '0';
            
            setTimeout(() => {
                progressSpan.textContent = `${newProgress}/${total}`;
                progressSpan.style.opacity = '1';
                
                // Update all progress bars after the text has been updated
                updateAllProgress();
                
                // If progress is complete, let animations finish then refresh
                if (newProgress === total) {
                    setTimeout(function() { 
                        window.location.reload(); 
                    }, 1500);
                }
            }, 300);

            if (newProgress === total) {
                console.log("Objective completed!");
                // Add completion animation
                objectiveCard.classList.add('completed-objective');
                
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
                    .then(() => {
                        // Update progress one final time after saving the note
                        updateAllProgress();
                    })
                    .catch(error => console.error("Error saving objective note:", error));
                } else {
                    // Update progress even if no note was provided
                    updateAllProgress();
                }
            }
        } else {
            console.error("Server returned error:", data.message);
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error incrementing objective:", error);
        alert("Error updating objective. Please try again.");
    });
}

// Function to update progress bar dynamically with improved animation
function updateProgressBar(progressElement, newValue, maxValue) {
    // Set the max value first
    progressElement.max = maxValue;
    
    // Get the current value
    const initialValue = parseInt(progressElement.value) || 0;
    const step = (newValue - initialValue) / 30;
    let current = initialValue;

    // Clear any existing animation
    if (progressElement.animationInterval) {
        clearInterval(progressElement.animationInterval);
    }

    // Ensure immediate visual feedback
    progressElement.value = initialValue;
    
    // Start the animation
    progressElement.animationInterval = setInterval(() => {
        current += step;
        if ((step > 0 && current >= newValue) || (step < 0 && current <= newValue)) {
            progressElement.value = newValue;
            clearInterval(progressElement.animationInterval);
            delete progressElement.animationInterval;
        } else {
            progressElement.value = current;
        }
    }, 20);
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

//Page Authored by Theodore Armes and Lewis Farley 



