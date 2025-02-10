// Get elements
var modal = document.getElementById("profilePictureModal");
var btn = document.getElementById("selectProfilePictureBtn");
var closeBtn = document.getElementById("closeModal");
var confirmBtn = document.getElementById("confirmSelectionBtn");
var selectedImage = null;

// Open the modal when the button is clicked
btn.onclick = function() {
    modal.style.display = "block";
}

// Close the modal when the close button is clicked
closeBtn.onclick = function() {
    modal.style.display = "none";
}

// Close the modal if the user clicks anywhere outside the modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Handle image selection
var profileImages = document.querySelectorAll(".profile-image");
profileImages.forEach(function(image) {
    image.onclick = function() {
        // Deselect any previously selected image
        profileImages.forEach(function(img) {
            img.style.borderColor = "transparent";
        });

        // Select the clicked image
        image.style.borderColor = "#007BFF";
        selectedImage = image.getAttribute("data-image");

        // Set the hidden input field's value to the selected image
        document.getElementById("profilePictureInput").value = selectedImage;
    }
});

// Confirm the selection and close the modal
confirmBtn.onclick = function() {
    if (selectedImage) {
        // Close the modal
        modal.style.display = "none";
    } else {
        alert("Please select a profile picture.");
    }
}
