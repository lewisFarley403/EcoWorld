// document.addEventListener("DOMContentLoaded", () => {
//     function createLeaf() {
//         let leaf = document.createElement("img");
//         leaf.src = "/static/guides/leaves/leaf" + (Math.floor(Math.random() * 4) + 1) + ".png"; // Random leaf image
//         leaf.classList.add("leaf");
//
//         // Set random position, size, and animation properties
//         leaf.style.left = Math.random() * 100 + "vw"; // Random left position
//         leaf.style.top = "-10%"; // Start above viewport
//         leaf.style.width = Math.random() * 20 + 30 + "px"; // Random width between 30px and 50px
//         leaf.style.animationDuration = Math.random() * 5 + 6 + "s"; // Between 6s and 11s
//         leaf.style.animationDelay = "0s"; // No delay for continuous effect
//         rotation = Math.random() * 720 - 360;
//         leaf.style.setProperty("--rotation", `${rotation}deg`);
//
//         document.body.appendChild(leaf);
//
//         // Remove the leaf after it falls
//         leaf.addEventListener("animationend", () => {
//             leaf.remove();
//         });
//     }
//
//     // Generate a new leaf every .6 seconds (adjust as needed)
//     setInterval(createLeaf, 600);
// });