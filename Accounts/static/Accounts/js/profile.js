document.addEventListener('DOMContentLoaded', function() {
    const pfpOptions = ['pfp1.png', 'pfp2.png', 'pfp3.png', 'pfp4.png', 'pfp5.png'];
    const btn = document.getElementById("selectProfilePictureBtn");

    if (btn) {
        btn.onclick = function() {
            const randomPfp = pfpOptions[Math.floor(Math.random() * pfpOptions.length)];
            const timestamp = new Date().getTime();

            const profilePicInput = document.getElementById("profilePictureInput");
            const profilePic = document.querySelector('.profile-picture');

            if (profilePicInput && profilePic) {
                profilePicInput.value = randomPfp;
                profilePic.src = `/media/pfps/${randomPfp}?v=${timestamp}`;
            }
        }
    }
});