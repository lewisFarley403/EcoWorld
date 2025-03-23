document.addEventListener("DOMContentLoaded", function () {
    // DOM Elements
    const latitudeInput = document.getElementById("latitude");
    const longitudeInput = document.getElementById("longitude");
    const postcodeInput = document.getElementById("postcode");
    const displayLatitude = document.getElementById("display-latitude");
    const displayLongitude = document.getElementById("display-longitude");
    const displayPostcode = document.getElementById("display-postcode");
    const postcodeSearchInput = document.getElementById("postcode-input");
    const postcodeSearchBtn = document.getElementById("postcode-search-btn");

    // Map Initialization
    const map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    let marker = null;

    // Update Display Function
    function updateDisplay() {
        displayLatitude.textContent = `Latitude: ${latitudeInput.value || "Not selected"}`;
        displayLongitude.textContent = `Longitude: ${longitudeInput.value || "Not selected"}`;
        displayPostcode.textContent = `Postcode: ${postcodeInput.value || "Not found"}`;
    }

    // Reverse Geocoding (Coordinates to Postcode)
    async function reverseGeocode(lat, lng) {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
            );
            const data = await response.json();
            const postcode = data.address?.postcode || "Not found";
            postcodeInput.value = postcode;
            updateDisplay();
        } catch (error) {
            console.error("Reverse geocoding failed:", error);
            displayPostcode.textContent = "Postcode: Error";
        }
    }

    // Handle Map Clicks
    map.on('click', async function(e) {
        const { lat, lng } = e.latlng;

        // Update or create marker
        if (marker) {
            marker.setLatLng(e.latlng);
        } else {
            marker = L.marker(e.latlng).addTo(map);
        }

        // Update form fields
        latitudeInput.value = lat;
        longitudeInput.value = lng;
        await reverseGeocode(lat, lng);
    });

    // Handle Postcode Search
    async function handlePostcodeSearch() {
        const postcode = postcodeSearchInput.value.trim();
        if (!postcode) return;

        try {
            // Forward geocoding
            const response = await fetch(
                `https://nominatim.openstreetmap.org/search?format=json&postalcode=${encodeURIComponent(postcode)}&country=GB&limit=1`
            );
            const data = await response.json();

            if (data.length === 0) {
                alert("Postcode not found. Please try another.");
                return;
            }

            const lat = parseFloat(data[0].lat);
            const lng = parseFloat(data[0].lon);

            // Update map view
            map.setView([lat, lng], 15);

            // Update marker position
            if (marker) {
                marker.setLatLng([lat, lng]);
            } else {
                marker = L.marker([lat, lng]).addTo(map);
            }

            // Update form fields
            latitudeInput.value = lat;
            longitudeInput.value = lng;
            postcodeInput.value = postcode;
            updateDisplay();

        } catch (error) {
            console.error("Postcode search failed:", error);
            alert("Error searching postcode. Please try again.");
        }
    }

    // Event Listeners
    postcodeSearchBtn.addEventListener("click", handlePostcodeSearch);
    postcodeSearchInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            handlePostcodeSearch();
        }
    });

    // Initial display setup
    updateDisplay();
});