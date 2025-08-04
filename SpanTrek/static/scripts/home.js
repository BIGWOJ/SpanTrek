// Home page JavaScript functionality for SpanTrek
document.addEventListener("DOMContentLoaded", function () {
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
        const targetWidth = bar.style.width;
        bar.style.width = "0%";
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 500);
    });

    // Add hover effect to streak flame
    const streakFlame = document.querySelector(".streak-flame");
    if (streakFlame) {
        streakFlame.addEventListener("mouseenter", function () {
            this.style.transform = "scale(1.3) rotate(10deg)";
        });

        streakFlame.addEventListener("mouseleave", function () {
            this.style.transform = "";
        });
    }

    // Daily challenge interaction
    const challengeCard = document.querySelector(".challenge-card");
    if (challengeCard) {
        challengeCard.addEventListener("click", function () {
            showNotification(
                "Keep going! Complete one more lesson to finish your daily challenge! 💪"
            );

            // Add a pulse effect
            this.style.animation = "pulse 0.6s ease";
            setTimeout(() => {
                this.style.animation = "";
            }, 600);
        });
    }

    // Continue button functionality
    const continueBtn = document.querySelector(".continue-btn");
    if (continueBtn) {
        continueBtn.addEventListener("click", function (e) {
            e.stopPropagation(); // Prevent card click
            showNotification(
                "Continuing with Family Members lesson! ¡Vamos! 👨‍👩‍👧‍👦"
            );

            // Simulate lesson loading
            this.textContent = "Loading...";
            this.disabled = true;

            setTimeout(() => {
                this.textContent = "Continue";
                this.disabled = false;
            }, 2000);
        });
    }

    // Add XP counter animation
    const xpText = document.querySelector(".xp-text");
    if (xpText) {
        xpText.addEventListener("click", function () {
            animateXPGain(50);
        });
    }
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

// Function to animate XP gain
function animateXPGain(xpAmount) {
    const xpText = document.querySelector(".xp-text");
    const currentXP = parseInt(
        xpText.textContent.replace(" XP", "").replace(",", "")
    );
    const newXP = currentXP + xpAmount;

    // Create floating XP indicator
    const floatingXP = document.createElement("div");
    floatingXP.textContent = `+${xpAmount} XP`;
    floatingXP.style.cssText = `
        position: absolute;
        top: 50%;
        right: 20px;
        color: #27ae60;
        font-weight: bold;
        font-size: 1.2rem;
        pointer-events: none;
        animation: floatUp 2s ease-out;
        z-index: 100;
    `;

    // Add float animation
    const floatStyle = document.createElement("style");
    floatStyle.textContent = `
        @keyframes floatUp {
            0% {
                transform: translateY(0);
                opacity: 1;
            }
            100% {
                transform: translateY(-50px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(floatStyle);

    // Add to XP section
    const levelCard = document.querySelector(".level-card");
    levelCard.style.position = "relative";
    levelCard.appendChild(floatingXP);

    // Animate XP counter
    let startXP = currentXP;
    const duration = 1000; // 1 second
    const startTime = Date.now();

    function updateXP() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const currentDisplayXP = Math.floor(startXP + xpAmount * progress);

        xpText.textContent = currentDisplayXP.toLocaleString() + " XP";

        if (progress < 1) {
            requestAnimationFrame(updateXP);
        }
    }

    updateXP();

    // Remove floating XP after animation
    setTimeout(() => {
        floatingXP.remove();
    }, 2000);

    showNotification(`Great! You earned ${xpAmount} XP! 🌟`);
}

// Add some fun easter eggs
let clickCount = 0;
document.addEventListener("click", function () {
    clickCount++;

    // Easter egg after 10 clicks
    if (clickCount === 10) {
        showNotification("¡Wow! You are really engaged! Keep learning! 🎉");
    }

    // Reset counter after some time
    setTimeout(() => {
        clickCount = Math.max(0, clickCount - 1);
    }, 5000);
});

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
