document.addEventListener("DOMContentLoaded", function() {
    const boxes = document.querySelectorAll(".answer-box");
    let selectedAnswers = {};

    boxes.forEach(box => {
        box.addEventListener("click", function() {
            let question = this.getAttribute("data-question");
            let value = this.getAttribute("data-value");
            let isMulti = this.hasAttribute("data-multi");

            if (!selectedAnswers[question]) {
                selectedAnswers[question] = new Set();
            }

            if (isMulti) {
                // Toggle selection for multiple choice questions
                if (selectedAnswers[question].has(value)) {
                    selectedAnswers[question].delete(value);
                    this.classList.remove("selected");
                } else {
                    selectedAnswers[question].add(value);
                    this.classList.add("selected");
                }
            } else {
                // Remove selection from other options in single-choice questions
                document.querySelectorAll(`[data-question="${question}"]`).forEach(item => {
                    item.classList.remove("selected");
                });

                selectedAnswers[question].clear();
                selectedAnswers[question].add(value);
                this.classList.add("selected");
            }
        });
    });

    window.submitQuiz = function() {
        let score = 0;
        let correctAnswers = {
            q1: new Set(["B", "D"]),
            q2: new Set(["B"])
            // Need to add more answers when I add Qs
        };

        for (let key in correctAnswers) {
            if (selectedAnswers[key]) {
                if (
                    correctAnswers[key].size === selectedAnswers[key].size &&
                    [...correctAnswers[key]].every(ans => selectedAnswers[key].has(ans))
                ) {
                    score++;
                }
            }
        }

        alert("Your score: " + score + "/" + Object.keys(correctAnswers).length);
    };
});