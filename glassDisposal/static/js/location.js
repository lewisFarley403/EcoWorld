function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function successCallback(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    //your What3Words API Key
    const apiKey = "PAX0KSR0";
    const apiUrl = `https://api.what3words.com/v3/convert-to-3wa?coordinates=${latitude},${longitude}&key=${apiKey}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.words) {
                document.getElementById("id_location").value = data.words;
            } else {
                alert("Could not fetch What3Words location.");
            }
        })
        .catch(error => {
            console.error("Error fetching What3Words data:", error);
        });
}

function errorCallback(error) {
    alert("Error getting location: " + error.message);
}