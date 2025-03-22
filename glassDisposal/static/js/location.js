// Wait for the entire HTML document to load before running the script
document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the button that triggers geolocation retrieval by its ID
    const locationButton = document.getElementById("get-location-btn");

    // Attach a click event listener to the location button
    locationButton.addEventListener("click", function () {
        // Check if the browser supports the Geolocation API
        if (navigator.geolocation) {
            // Request the current position. If successful, successCallback is called; if there's an error, errorCallback is called.
            navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
        } else {
            // Alert the user if geolocation is not supported by their browser
            alert("Geolocation is not supported by this browser.");
        }
    });
});

// Callback function executed when the geolocation is successfully retrieved
function successCallback(position) {
    // Extract the latitude and longitude values from the position object provided by the Geolocation API
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Update the hidden input fields in the form with the retrieved latitude and longitude values
    document.getElementById("latitude").value = latitude;
    document.getElementById("longitude").value = longitude;

    // Notify the user that their location has been successfully set, displaying the coordinates
    alert(`Location set! Lat: ${latitude}, Lon: ${longitude}`);
}

// Callback function executed when there is an error retrieving the geolocation
function errorCallback(error) {
    // Log the error details to the console for debugging purposes
    console.error("Error retrieving location:", error);
    // Alert the user that the location could not be retrieved and suggest allowing location access
    alert("Unable to retrieve location. Please allow location access.");
}
