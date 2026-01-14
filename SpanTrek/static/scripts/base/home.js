document.addEventListener("DOMContentLoaded", function () {
    // Daily challenges tooltip
    const challengeTooltip = document.createElement("div");
    challengeTooltip.className = "challenge-tooltip";
    document.body.appendChild(challengeTooltip);

    const challengeSteps = document.querySelectorAll(".challenge-step");
    challengeSteps.forEach((step) => {
        step.addEventListener("mousemove", showChallengeTooltip);
        step.addEventListener("mouseleave", hideChallengeTooltip);
    });

    // Show tooltip
    function showChallengeTooltip(e) {
        const step = e.target;
        const description = step.getAttribute("challenge-description");

        if (description) {
            challengeTooltip.innerHTML = description;

            const rect = step.getBoundingClientRect();
            const scrollTop =
                window.scrollY || document.documentElement.scrollTop;
            const scrollLeft =
                window.scrollX || document.documentElement.scrollLeft;

            const tooltipX = rect.left + rect.width / 2 + scrollLeft;
            const tooltipY = rect.top + scrollTop - 10;

            challengeTooltip.style.left = `${tooltipX}px`;
            challengeTooltip.style.top = `${tooltipY}px`;
            challengeTooltip.classList.add("visible");
        }
    }

    // Hide tooltip
    function hideChallengeTooltip() {
        challengeTooltip.classList.remove("visible");
    }

    // Animate progress bars on page load
    const progressBars = document.querySelectorAll(".progress-fill");
    progressBars.forEach((bar) => {
        const targetWidth = bar.style.width;

        bar.style.width = "0%";
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 500);
    });
});

