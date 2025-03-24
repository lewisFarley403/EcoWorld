function isMobileDevice() {
    return window.matchMedia("(max-width: 768px)").matches;
}

function disableTooltipOnMobile() {
    if (isMobileDevice()) {
        const tooltip = document.getElementById("tooltip");
        if (tooltip) {
            tooltip.style.display = "none";
            tooltip.style.visibility = "hidden";
        }
    }
}

function onPageLoad() {
    // Handle back button and page restore
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            disableTooltipOnMobile();
        }
    });

    

    // Handle visibility changes
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            disableTooltipOnMobile();
        }
    });

    // Fetch leaderboard data from the server
    fetch('getleaderboarddata').then(response => response.json()).then(data => {

        // If there are fewer than 3 players, we just take whatever is available
        let top3 = data.rankedUsers.length < 3 ? data.rankedUsers : data.rankedUsers.slice(0, 3);

        // Clear all positions first
        document.getElementById('firstPfp').src = '';
        document.getElementById('firstName').innerText = '';
        document.getElementById('firstScore').innerText = '0';
        
        document.getElementById('secondPfp').src = '';
        document.getElementById('secondName').innerText = '';
        document.getElementById('secondScore').innerText = '0';
        
        document.getElementById('thirdPfp').src = '';
        document.getElementById('thirdName').innerText = '';
        document.getElementById('thirdScore').innerText = '0';

        // First place goes in the middle
        if (top3.length >= 1) {
            document.getElementById('firstPfp').src = top3[0].pfp_url; 
            document.getElementById('firstName').innerText = top3[0].username;
            document.getElementById('firstScore').innerText = top3[0].score;
        }

        // Second place
        if (top3.length >= 2) {
            document.getElementById('secondPfp').src = top3[1].pfp_url;
            document.getElementById('secondName').innerText = top3[1].username;
            document.getElementById('secondScore').innerText = top3[1].score;
        }

        // Third place
        if (top3.length >= 3) {
            document.getElementById('thirdPfp').src = top3[2].pfp_url;
            document.getElementById('thirdName').innerText = top3[2].username;
            document.getElementById('thirdScore').innerText = top3[2].score;
        }

        var table = document.getElementById("leaderboard-body");
        var tooltip = document.getElementById("tooltip");
        
        // Only setup tooltip if not on mobile
        if (!isMobileDevice()) {
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
        } else {
            // Hide tooltip element completely on mobile
            tooltip.style.display = "none";
            tooltip.style.visibility = "hidden";
        }

        data.rankedUsers.forEach((user, i) => {
            var row = table.insertRow(-1);
            
            // row.href = `/read_profile/?username=${user.username}`;
            row.addEventListener("click", () => {
                window.location.href = `/read_profile/?username=${user.username}`;
            });
        
            // Add the link to the row
            if (!isMobileDevice()) {
                row.addEventListener("mouseenter", async (event) => {
                    if (isMobileDevice()) return; // Double-check for mobile
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
                    if (isMobileDevice()) return; // Double-check for mobile
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
        document.getElementById('current-rank').innerText = logged_in_user_rank;
        document.getElementById('current-coins').innerText = logged_in_user_score;
        document.getElementById('current-name').innerText = logged_in_user_username;
    }).catch((error) => {
        console.error('Error fetching leaderboard data:', error);
    });
}

onPageLoad();


