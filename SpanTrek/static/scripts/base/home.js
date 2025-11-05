// Home page JavaScript functionality
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
            
            // Position tooltip
            const rect = step.getBoundingClientRect();
            const scrollTop = window.scrollY || document.documentElement.scrollTop;
            const scrollLeft = window.scrollX || document.documentElement.scrollLeft;

            // Calculate position above the step element
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

    // Add click animations to lesson cards
    const lessonCards = document.querySelectorAll(".lesson-card");
    lessonCards.forEach((card) => {
        card.addEventListener("click", function () {
            if (!this.classList.contains("locked")) {
                this.style.transform = "scale(0.95)";
                setTimeout(() => {
                    this.style.transform = "";
                }, 150);

                // Simulate lesson start (you can replace with actual navigation)
                if (this.classList.contains("current")) {
                    showNotification(
                        "Starting lesson: " +
                            this.querySelector("h4").textContent +
                            "! 🚀"
                    );
                } else if (this.classList.contains("completed")) {
                    showNotification(
                        "Reviewing: " +
                            this.querySelector("h4").textContent +
                            " 📚"
                    );
                }
            }
        });
    });

    // Add functionality to action buttons
    const actionButtons = document.querySelectorAll(".action-btn");
    actionButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const action = this.querySelector("span").textContent;
            showNotification(`${action} mode coming soon! 🎯`);

            // Add a bounce animation
            this.style.animation = "bounce 0.6s ease";
            setTimeout(() => {
                this.style.animation = "";
            }, 600);
        });
    });

    // Animate progress bars on page load
    const progressBars = document.querySelectorAll(".progress-fill");
    progressBars.forEach((bar) => {
        // Get the target width from the inline style set by Django
        const targetWidth = bar.style.width;
        
        // Start from 0% and animate to target
        bar.style.width = "0%";
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 500);
    });
});

// Function to show notifications
function showNotification(message) {
    // Remove existing notification if any
    const existingNotification = document.querySelector(".notification");
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement("div");
    notification.className = "notification";
    notification.textContent = message;

    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #27ae60;
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        font-weight: bold;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;

    // Add CSS animation
    const style = document.createElement("style");
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
    `;
    document.head.appendChild(style);

    // Add to page
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = "slideOutRight 0.3s ease";
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add keyboard shortcuts
document.addEventListener("keydown", function (e) {
    // Press 'C' to continue current lesson
    if (e.key.toLowerCase() === "c" && !e.ctrlKey && !e.altKey) {
        const continueBtn = document.querySelector(".continue-btn");
        if (continueBtn) {
            continueBtn.click();
        }
    }

    // Press 'P' for practice
    if (e.key.toLowerCase() === "p" && !e.ctrlKey && !e.altKey) {
        const practiceBtn = document.querySelector(".action-btn.practice");
        if (practiceBtn) {
            practiceBtn.click();
        }
    }
});

// Add loading animation for lesson cards
function addLoadingAnimation(card) {
    card.style.opacity = "0.7";
    card.style.pointerEvents = "none";

    const loadingSpinner = document.createElement("div");
    loadingSpinner.innerHTML = "⏳";
    loadingSpinner.style.cssText = `
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 2rem;
        animation: spin 1s linear infinite;
    `;

    const spinStyle = document.createElement("style");
    spinStyle.textContent = `
        @keyframes spin {
            from { transform: translate(-50%, -50%) rotate(0deg); }
            to { transform: translate(-50%, -50%) rotate(360deg); }
        }
    `;
    document.head.appendChild(spinStyle);

    card.style.position = "relative";
    card.appendChild(loadingSpinner);

    // Remove loading after 2 seconds
    setTimeout(() => {
        card.style.opacity = "";
        card.style.pointerEvents = "";
        loadingSpinner.remove();
    }, 2000);
}
