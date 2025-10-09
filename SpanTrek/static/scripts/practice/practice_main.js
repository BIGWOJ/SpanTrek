document.addEventListener("DOMContentLoaded", function () {
    const userInput = document.getElementById("userInput");
    const checkBtn = document.querySelector(".check-btn-input");
    const resetBtn = document.querySelector(".reset-btn-input");

    // Get correct answer from data attribute
    const correctAnswer = userInput.getAttribute("data-answer") || "";

    // Check answer functionality
    checkBtn.addEventListener("click", function () {
        const userAnswer = userInput.value.trim();

        // Don't check if no answer is provided
        if (userAnswer === "") return;

        // Remove previous classes
        userInput.classList.remove("correct", "incorrect");

        // Check if answer is correct (case-insensitive comparison)
        if (userAnswer.toLowerCase() === correctAnswer.toLowerCase()) {
            userInput.classList.add("correct");
            checkBtn.style.background = "rgba(76, 175, 80, 0.2)";
            checkBtn.style.borderColor = "#4caf50";
            checkBtn.style.color = "#4caf50";
            checkBtn.textContent = "Perfect!";

            // Show the next button when exercise is completed successfully
            const nextBtn = document.querySelector(".next-btn");
            if (nextBtn) {
                // Auto-advance to next exercise after 2 seconds
                setTimeout(() => {
                    nextBtn.click();
                }, 500);
            }
        } else {
            userInput.classList.add("incorrect");
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
        userInput.value = "";

        // Remove state classes
        userInput.classList.remove("correct", "incorrect");

        // Reset button
        checkBtn.style.background = "";
        checkBtn.style.borderColor = "";
        checkBtn.style.color = "";
        checkBtn.textContent = "Check answer";

        // Hide the next button when resetting
        const nextBtn = document.querySelector(".next-btn");
        if (nextBtn) {
            nextBtn.style.display = "none";
        }

        // Add brief highlight effect
        userInput.style.transition = "all 0.3s ease";
        userInput.style.backgroundColor = "rgba(255, 165, 31, 0.2)";

        setTimeout(() => {
            userInput.style.backgroundColor = "";
        }, 300);

        // Focus back to input
        userInput.focus();
    });

    // Clear states when user starts typing
    userInput.addEventListener("input", function () {
        this.classList.remove("correct", "incorrect");

        // Hide next button when user starts typing again
        const nextBtn = document.querySelector(".next-btn");
        if (nextBtn) {
            nextBtn.style.display = "none";
        }
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
    });

    // Enter key specifically for input field
    userInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            if (checkBtn && !checkBtn.disabled) {
                checkBtn.click();
            }
        }
    });

    // Auto-focus on input when page loads
    userInput.focus();
});
