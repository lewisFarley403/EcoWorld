document.addEventListener("DOMContentLoaded", function () {
    const paragraphDisplay = document.getElementById("paragraph-display");
    const prevButton = document.getElementById("prev-button");
    const nextButton = document.getElementById("next-button");
    const progressBar = document.getElementById("progress-bar");

    let index = 0;

    function updateProgressBar() {
        const progress = ((index + 1) / paragraphs.length) * 100;
        progressBar.style.width = `${progress}%`;
    }

    function nextParagraph() {
        if (index < paragraphs.length - 1) {
            index++;
            paragraphDisplay.innerText = paragraphs[index];
            updateProgressBar();
        }
        else {
            index = 0;
            paragraphDisplay.innerText = paragraphs[index];
            updateProgressBar();
        }
    }

    function prevParagraph() {
        if (index > 0) {
            index--;
            paragraphDisplay.innerText = paragraphs[index];
            updateProgressBar();
        }
        else {
            index = paragraphs.length - 1;
            paragraphDisplay.innerText = paragraphs[index];
            updateProgressBar();
        }
    }

    prevButton.addEventListener("click", prevParagraph);
    nextButton.addEventListener("click", nextParagraph);

    updateProgressBar();
});