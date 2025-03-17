document.addEventListener("DOMContentLoaded", function () {
    const locationButton = document.getElementById("get-location-btn");

    locationButton.addEventListener("click", function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });
});

function successCallback(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    document.getElementById("latitude").value = latitude;
    document.getElementById("longitude").value = longitude;

    alert(`Location set! Lat: ${latitude}, Lon: ${longitude}`);
}

function errorCallback(error) {
    console.error("Error retrieving location:", error);
    alert("Unable to retrieve location. Please allow location access.");
}

