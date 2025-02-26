alert("Script loaded");

// Get elements
var modal = document.getElementById("profilePictureModal");
var btn = document.getElementById("selectProfilePictureBtn");
var closeBtn = document.getElementById("closeModal");
var confirmBtn = document.getElementById("confirmSelectionBtn");
var selectedImage = null;
var profileImages = document.querySelectorAll(".profile-image");

// Open the modal when the button is clicked
btn.onclick = function() {
    modal.style.display = "block";
}

// Close the modal when the close button is clicked
closeBtn.onclick = function() {
    modal.style.display = "none";
}

// Close the modal if the user clicks outside
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Handle image selection
profileImages.forEach(function(image) {
    image.onclick = function() {
        console.log("Image clicked!");

        // Deselect any previously selected image
        profileImages.forEach(function(img) {
            img.style.borderColor = "transparent";
        });

        // Select the clicked image
        image.style.borderColor = "#00a6ff";
        selectedImage = image.getAttribute("data-image");

        // Set the hidden input field's value
        document.getElementById("profilePictureInput").value = selectedImage;

        // Close the modal
        modal.style.display = "none";
    }
});

// Confirm selection and close modal
confirmBtn.onclick = function() {
    if (selectedImage) {
        modal.style.display = "none";
    } else {
        alert("Please select a profile picture.");
    }
}
