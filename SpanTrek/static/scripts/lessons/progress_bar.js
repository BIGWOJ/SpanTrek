document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.querySelector(".progress-bar .progress-fill");
    const progressText = document.querySelector(".progress-bar-text");
    if (progressBar) {
        // Get user progress and total lessons from the text
        // Example: "3 / 5 lessons completed"
        const progressInfo = document.querySelector(".progress-bar-info");
        let userProgress = 0,
            totalLessons = 1;
        if (progressInfo) {
            const match = progressInfo.textContent.match(/(\d+)\s*\/\s*(\d+)/);
            if (match) {
                userProgress = parseInt(match[1]);
                totalLessons = parseInt(match[2]);
            }
        }
        const percent = Math.round((userProgress / totalLessons) * 100) || 0;

        progressBar.style.width = "0%";
        setTimeout(() => {
            progressBar.style.width = percent + "%";
        }, 500);
        if (progressText) {
            progressText.textContent = percent + "%";
        }
    }
});
