document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.querySelector(".check-btn-fill");
    const resetBtn = document.querySelector(".reset-btn-fill");
    const blankInputs = document.querySelectorAll(".blank-input");

    // Check answers functionality
    checkBtn.addEventListener("click", function () {
        let userAnswered = false;
        blankInputs.forEach((input) => {
            if (input.value.trim() !== "") {
                userAnswered = true;
            }
        });
        blankInputs.forEach((input) => {
            const userAnswer = input.value.trim().toLowerCase();
            const correctAnswer = input
                .getAttribute("data-answer")
                .toLowerCase();

            // Remove previous classes
            input.classList.remove("correct", "incorrect");

            // Add appropriate class based on answer
            if (userAnswer === correctAnswer) {
                input.classList.add("correct");
            } else if (userAnswer !== "") {
                input.classList.add("incorrect");
            }
        });
        const allCorrect = Array.from(blankInputs).every((input) =>
            input.classList.contains("correct")
        );

        // Don't check if no choices are selected
        if (!userAnswered) return;

        if (allCorrect) {
            // All correct answers selected, no incorrect ones
            checkBtn.style.background = "rgba(76, 175, 80, 0.2)";
            checkBtn.style.borderColor = "#4caf50";
            checkBtn.style.color = "#4caf50";
            checkBtn.textContent = "Perfect!";
        } else {
            // Show red "Try again" state temporarily for 2 seconds
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
        blankInputs.forEach((input) => {
            // Clear the input value
            input.value = "";

            // Remove all state classes
            input.classList.remove("correct", "incorrect");

            // Optional: Add a brief highlight effect to show reset
            input.style.transition = "all 0.3s ease";
            input.style.backgroundColor = "rgba(255, 165, 31, 0.2)";

            setTimeout(() => {
                input.style.backgroundColor = "";
            }, 300);
        });

        // Reset check button to default state
        checkBtn.style.background = "";
        checkBtn.style.borderColor = "";
        checkBtn.style.color = "";
        checkBtn.textContent = "Check answers";
    });

    // Optional: Clear states when user starts typing again
    blankInputs.forEach((input) => {
        input.addEventListener("input", function () {
            this.classList.remove("correct", "incorrect");
        });
    });

    document.addEventListener("keydown", function (event) {
        // Handle Enter key for check button
        if (event.key === "Enter") {
            // event.preventDefault();
            if (checkBtn && !checkBtn.disabled) {
                checkBtn.click();
            }
            return;
        }

        // Handle Delete key for reset button
        if (event.key === "Delete") {
            event.preventDefault();
            if (resetBtn && !resetBtn.disabled) {
                resetBtn.click();
            }
            return;
        }
    });

    // Additional Enter key handler specifically for input fields
    blankInputs.forEach((input) => {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                if (checkBtn && !checkBtn.disabled) {
                    checkBtn.click();
                }
            }
        });
    });
});
