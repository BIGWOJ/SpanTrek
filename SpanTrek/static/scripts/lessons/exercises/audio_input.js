document.addEventListener("DOMContentLoaded", function () {
    const playPauseBtn = document.getElementById("playPauseBtn");
    const playIcon = document.querySelector(".play-icon");
    const pauseIcon = document.querySelector(".pause-icon");
    const audioInput = document.getElementById("audioInput");
    const checkBtn = document.querySelector(".check-btn-audio");
    const resetBtn = document.querySelector(".reset-btn-audio");
    const progressFill = document.querySelector(".progress-fill");
    const audioPlayer = document.querySelector(".audio-player");

    let isPlaying = false;
    let audio = null; // Will be set when audio file is loaded

    // Example correct answer - this would typically come from the backend
    const correctAnswer = "hello world"; // Replace with actual answer

    // Play/Pause functionality
    playPauseBtn.addEventListener("click", function () {
        if (!audio) {
            // Create audio element if not exists
            // audio = new Audio('path/to/your/audio/file.mp3');
            console.log("Audio file not loaded yet");
            return;
        }

        if (isPlaying) {
            audio.pause();
            pauseAudio();
        } else {
            audio.play();
            playAudio();
        }
    });

    function playAudio() {
        isPlaying = true;
        playIcon.style.display = "none";
        pauseIcon.style.display = "block";
        audioPlayer.classList.add("playing");
    }

    function pauseAudio() {
        isPlaying = false;
        playIcon.style.display = "block";
        pauseIcon.style.display = "none";
        audioPlayer.classList.remove("playing");
    }

    // Check answer functionality
    checkBtn.addEventListener("click", function () {
        const userAnswer = audioInput.value.trim().toLowerCase();

        // Don't check if no answer is provided
        if (userAnswer === "") return;

        // Remove previous classes
        audioInput.classList.remove("correct", "incorrect");

        // Check if answer is correct
        if (userAnswer === correctAnswer.toLowerCase()) {
            audioInput.classList.add("correct");
            checkBtn.style.background = "rgba(76, 175, 80, 0.2)";
            checkBtn.style.borderColor = "#4caf50";
            checkBtn.style.color = "#4caf50";
            checkBtn.textContent = "Perfect!";
        } else {
            audioInput.classList.add("incorrect");
            checkBtn.style.background = "rgba(244, 67, 54, 0.2)";
            checkBtn.style.borderColor = "#f44336";
            checkBtn.style.color = "#f44336";
            checkBtn.textContent = "Try again";

            // Reset button appearance after 2 seconds
            setTimeout(() => {
                checkBtn.style.background = "";
                checkBtn.style.borderColor = "";
                checkBtn.style.color = "";
                checkBtn.textContent = "Check answer";
            }, 2000);
        }
    });

    // Reset functionality
    resetBtn.addEventListener("click", function () {
        // Clear input
        audioInput.value = "";

        // Remove state classes
        audioInput.classList.remove("correct", "incorrect");

        // Reset button
        checkBtn.style.background = "";
        checkBtn.style.borderColor = "";
        checkBtn.style.color = "";
        checkBtn.textContent = "Check answer";

        // Add brief highlight effect
        audioInput.style.transition = "all 0.3s ease";
        audioInput.style.backgroundColor = "rgba(255, 165, 31, 0.2)";

        setTimeout(() => {
            audioInput.style.backgroundColor = "";
        }, 300);

        // Reset audio if playing
        if (audio && isPlaying) {
            audio.pause();
            audio.currentTime = 0;
            pauseAudio();
        }
    });

    // Clear states when user starts typing
    audioInput.addEventListener("input", function () {
        this.classList.remove("correct", "incorrect");
    });

    // Keyboard navigation
    document.addEventListener("keydown", function (event) {
        const code = event.code;

        // Handle Enter key (both main Enter and numpad Enter)
        if (event.key === "Enter" || code === "NumpadEnter") {
            event.preventDefault();
            if (checkBtn && !checkBtn.disabled) {
                checkBtn.click();
            }
            return;
        }

        // Handle Delete key (both main Delete and numpad Delete/Decimal)
        if (
            event.key === "Delete" ||
            code === "NumpadDelete" ||
            code === "NumpadDecimal"
        ) {
            event.preventDefault();
            if (resetBtn && !resetBtn.disabled) {
                resetBtn.click();
            }
            return;
        }

        // Handle Space key for play/pause
        if (event.key === " " || event.key === "Spacebar") {
            // Only if input is not focused
            if (document.activeElement !== audioInput) {
                event.preventDefault();
                playPauseBtn.click();
            }
            return;
        }
    });

    // Enter key specifically for input field
    audioInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            if (checkBtn && !checkBtn.disabled) {
                checkBtn.click();
            }
        }
    });

    // Progress bar click functionality
    const progressBar = document.querySelector(".progress-bar");
    progressBar.addEventListener("click", function (e) {
        if (audio) {
            const rect = progressBar.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const width = rect.width;
            const percentage = (clickX / width) * 100;

            progressFill.style.width = percentage + "%";
            audio.currentTime = (percentage / 100) * audio.duration;
        }
    });

    // Update progress bar during playback
    if (audio) {
        audio.addEventListener("timeupdate", function () {
            const percentage = (audio.currentTime / audio.duration) * 100;
            progressFill.style.width = percentage + "%";
        });

        audio.addEventListener("ended", function () {
            pauseAudio();
            progressFill.style.width = "0%";
        });
    }
});
