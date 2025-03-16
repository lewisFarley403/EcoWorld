function isMobileDevice() {
    return window.matchMedia("(max-width: 768px)").matches;
}

function onPageLoad() {
    console.log("Document loaded");

    // Fetch leaderboard data from the server
    fetch('getleaderboarddata').then(response => response.json()).then(data => {
        console.log(data);

        // If there are fewer than 3 players, we just take whatever is available
        let top3 = data.rankedUsers.length < 3 ? data.rankedUsers : data.rankedUsers.slice(0, 3);

        // First place goes in the middle
        if (top3.length >= 1) {
            document.getElementById('firstPfp').src = top3[1].pfp_url; 
            document.getElementById('firstName').innerText = top3[1].username;
        }

        // Second place goes in the left container
        if (top3.length >= 2) {
            document.getElementById('secondPfp').src = top3[0].pfp_url;
            document.getElementById('secondName').innerText = top3[0].username;
        }

        // Third place goes in the right container
        if (top3.length >= 3) {
            document.getElementById('thirdPfp').src = top3[2].pfp_url;
            document.getElementById('thirdName').innerText = top3[2].username;
        }

        // If there are fewer than 3 players, we can clear the unused places
        if (top3.length < 3) {
            if (top3.length < 2) {
                document.getElementById('secondPfp').src = '';
                document.getElementById('secondName').innerText = '';
            }
            if (top3.length < 1) {
                document.getElementById('thirdPfp').src = '';
                document.getElementById('thirdName').innerText = '';
            }
        }

        var table = document.getElementById("leaderboard-body");
        var tooltip = document.getElementById("tooltip");
        tooltip.style.position = "absolute";
        tooltip.style.background = "rgba(0, 0, 0, 0.8)";
        tooltip.style.background = "transparent";
        tooltip.style.color = "white";
        tooltip.style.padding = "5px 10px";
        tooltip.style.borderRadius = "5px";
        tooltip.style.fontSize = "12px";
        tooltip.style.display = "none";
        tooltip.style.pointerEvents = "none";
        tooltip.style.zIndex = "1000";
        data.rankedUsers.forEach((user, i) => {
            console.log("USER")
            console.log(user);
            var row = table.insertRow(-1);
            // row.href = `/read_profile/?username=${user.username}`;
            row.addEventListener("click", () => {
                window.location.href = `/read_profile/?username=${user.username}`;
            });
        
            // Add the link to the row
            if (!isMobileDevice()) {
                row.addEventListener("mouseenter", async (event) => {
                    let username = row.cells[1].innerText;
                    try {
                        let response = await fetch(`get-tooltip-template/?username=${username}`);
                        let html = await response.text();
                        tooltip.innerHTML = html;
                        tooltip.style.display = "block";
                    } catch (error) {
                        console.error("Error fetching tooltip template:", error);
                    }
                });
        
                row.addEventListener("mousemove", (event) => {
                    tooltip.style.top = `${event.clientY -350}px`;
                    tooltip.style.left = `${event.clientX + 10}px`;
                });
        
                row.addEventListener("mouseleave", () => {
                    tooltip.style.display = "none";
                });
            }

            var rank = row.insertCell(0);
            var username = row.insertCell(1);
            var score = row.insertCell(2);
            rank.innerHTML = i + 1;
            username.innerHTML = user.username;
            score.innerHTML = user.score;
        });
        const logged_in_user_rank = data.current_user_data.rank
        const logged_in_user_score = data.current_user_data.score
        const logged_in_user_username = data.current_user_data.username
        console.log(logged_in_user_score)
        document.getElementById('current-rank').innerText = logged_in_user_rank;
        document.getElementById('current-coins').innerText = logged_in_user_score;
        document.getElementById('current-name').innerText = logged_in_user_username;
    }).catch((error) => {
        console.error('Error fetching leaderboard data:', error);
    });
}

onPageLoad();


