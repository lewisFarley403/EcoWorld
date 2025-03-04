function onPageLoad() {
    console.log("Document loaded");

    // Fetch leaderboard data from the server
    fetch('getleaderboarddata').then(response => response.json()).then(data => {
        console.log(data);

        // If there are fewer than 3 players, we just take whatever is available
        let top3 = data.rankedUsers.length < 3 ? data.rankedUsers : data.rankedUsers.slice(0, 3);

        // First place goes in the middle
        if (top3.length >= 1) {
            document.getElementById('firstPfp').src = top3[0].pfp_url || '/path/to/default-profile-pic.png';  // Default profile pic if not available
            document.getElementById('firstName').innerText = top3[0].username;
        }

        // Second place goes in the left container
        if (top3.length >= 2) {
            document.getElementById('secondPfp').src = top3[1].pfp_url || '/path/to/default-profile-pic.png';
            document.getElementById('secondName').innerText = top3[1].username;
        }

        // Third place goes in the right container
        if (top3.length >= 3) {
            document.getElementById('thirdPfp').src = top3[2].pfp_url || '/path/to/default-profile-pic.png';
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

        // Optionally, populate the rest of the leaderboard in a table
        var table = document.getElementById("leaderboard-table");
        data.rankedUsers.forEach((user, i) => {
            var row = table.insertRow(-1);
            var rank = row.insertCell(0);
            var username = row.insertCell(1);
            var score = row.insertCell(2);
            rank.innerHTML = user.rank;
            username.innerHTML = user.username;
            score.innerHTML = user.score;
        });
    }).catch((error) => {
        console.error('Error fetching leaderboard data:', error);
    });
}
onPageLoad()