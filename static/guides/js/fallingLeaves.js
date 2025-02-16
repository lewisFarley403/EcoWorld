document.addEventListener("DOMContentLoaded", () => {
    function createLeaf() {
        let leaf = document.createElement("img");
        leaf.src = "/static/guides/leaves/leaf" + (Math.floor(Math.random() * 5) + 1) + ".png"; // Random leaf image
        leaf.classList.add("leaf");

        // Set random position, size, and animation properties
        leaf.style.left = Math.random() * 100 + "vw"; // Random left position
        leaf.style.top = "-10%"; // Start above viewport
        leaf.style.width = Math.random() * 20 + 30 + "px"; // Random width between 30px and 50px
        leaf.style.animationDuration = Math.random() * 5 + 5 + "s"; // Between 5s and 10s
        leaf.style.animationDelay = "0s"; // No delay for continuous effect

        document.body.appendChild(leaf);

        // Remove the leaf after it falls
        setTimeout(() => {
            leaf.remove();
        }, 12000);
    }

    // Generate a new leaf every 1 second (adjust as needed)
    setInterval(createLeaf, 1000);
});