document.addEventListener("DOMContentLoaded", function () {
    const playPauseBtn = document.getElementById("playPauseBtn");
    const playIcon = document.querySelector(".play-icon");
    const pauseIcon = document.querySelector(".pause-icon");
    const audioPlayer = document.querySelector(".audio-player");
    const progressFill = document.querySelector(".progress-fill-audio");
    const audioTitle = document.querySelector(".audio-title");
    const audioDuration = document.querySelector(".audio-duration");

    let audio = null;
    let isPlaying = false;

    // Initialize audio when page loads
    function initializeAudio() {
        // Get audio URL from the content variable
        const audioUrl = window.audioContentUrl;

        if (audioUrl && audioUrl !== "link_audio") {
            audio = new Audio(audioUrl);

            audio.addEventListener("loadedmetadata", function () {
                updateDuration();
            });

            audio.addEventListener("timeupdate", function () {
                updateProgress();
            });

            audio.addEventListener("ended", function () {
                stopAudio();
                resetProgress();
            });

            audio.addEventListener("error", function () {
                console.error("Error loading audio file:", audioUrl);
                audioTitle.textContent = "Audio Error";
            });
        } else {
            audioTitle.textContent = "No Audio Available";
            playPauseBtn.disabled = true;
            playPauseBtn.style.opacity = "0.5";
        }
    }

    // Play/Pause button
    playPauseBtn.addEventListener("click", function () {
        if (!audio) {
            return;
        }

        if (isPlaying) {
            stopAudio();
        } else {
            playAudio();
        }
    });

    function playAudio() {
        if (audio) {
            audio
                .play()
                .then(() => {
                    isPlaying = true;
                    playIcon.style.display = "none";
                    pauseIcon.style.display = "block";
                    audioPlayer.classList.add("playing");
                })
                .catch((error) => {
                    console.error("Error playing audio:", error);
                });
        }
    }

    function stopAudio() {
        if (audio) {
            audio.pause();
            isPlaying = false;
            playIcon.style.display = "block";
            pauseIcon.style.display = "none";
            audioPlayer.classList.remove("playing");
        }
    }

    function updateProgress() {
        if (audio && audio.duration) {
            const percentage = (audio.currentTime / audio.duration) * 100;
            progressFill.style.width = percentage + "%";

            // Update time display
            const currentTime = formatTime(audio.currentTime);
            const totalTime = formatTime(audio.duration);
            audioDuration.textContent = `${currentTime} / ${totalTime}`;
        }
    }

    function updateDuration() {
        if (audio && audio.duration) {
            const totalTime = formatTime(audio.duration);
            audioDuration.textContent = `0:00 / ${totalTime}`;
        }
    }

    function resetProgress() {
        progressFill.style.width = "0%";
        if (audio) {
            audio.currentTime = 0;
        }
    }

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
    }

    // Progress bar click functionality
    const progressBar = document.querySelector(".progress-bar");
    progressBar.addEventListener("click", function (e) {
        if (audio && audio.duration) {
            const rect = progressBar.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const width = rect.width;
            const percentage = clickX / width;

            audio.currentTime = percentage * audio.duration;
            updateProgress();
        }
    });

    // Initialize audio when page loads
    initializeAudio();
});
