document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.querySelector(".check-btn-fill");
    const resetBtn = document.querySelector(".reset-btn-fill");
    const showAnswerBtn = document.querySelector(".show-answer-btn-fill");
    const blankInputs = document.querySelectorAll(".blank-input");

    // Clear all input fields on page load
    blankInputs.forEach((input) => {
        input.value = "";
        input.classList.remove("correct", "incorrect");
    });

    // Set correct names for input fields
    blankInputs.forEach((input, index) => {
        input.name = `answer_${index + 1}`;
    });

    // Check answers
    checkBtn.addEventListener("click", function (event) {
        event.preventDefault();

        let userAnswered = false;
        blankInputs.forEach((input) => {
            if (input.value.trim() !== "") {
                userAnswered = true;
            }
        });

        // Don't check if no choices are selected
        if (!userAnswered) return;

        // Visual feedback
        blankInputs.forEach((input) => {
            const userAnswer = input.value.trim();
            const correctAnswer = input.getAttribute("data-answer");

            // Normalize and compare
            const normalizedUserAnswer = normalizeSpanishText(
                userAnswer.toLowerCase()
            );
            const normalizedCorrectAnswer = normalizeSpanishText(
                correctAnswer.toLowerCase()
            );

            input.classList.remove("correct", "incorrect");

            // Class based on answer
            if (normalizedUserAnswer === normalizedCorrectAnswer) {
                input.classList.add("correct");
            } else if (userAnswer !== "") {
                input.classList.add("incorrect");
            }
        });

        const allCorrect = Array.from(blankInputs).every((input) =>
            input.classList.contains("correct")
        );

        // Visual feedback
        if (allCorrect) {
            checkBtn.style.background = "rgba(76, 175, 80, 0.2)";
            checkBtn.style.borderColor = "#4caf50";
            checkBtn.style.color = "#4caf50";
            checkBtn.textContent = "Perfect!";

            // Show the next button only when exercise is completed successfully
            const nextBtn =
                document.getElementById("next-exercise-btn") ||
                document.getElementById("complete-lesson-btn");
            if (nextBtn) {
                nextBtn.style.display = "inline-block";
                nextBtn.style.opacity = "0";
                nextBtn.style.transition = "opacity 0.5s ease-in-out";
                setTimeout(() => {
                    nextBtn.style.opacity = "1";
                    nextBtn.style.transition = "all 0.3s ease";
                }, 100);
            }
        } else {
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

        sendAnswersToBackend(allCorrect);
    });

    // Send answers to backend
    function sendAnswersToBackend(allCorrect) {
        const form = document.querySelector("form");
        const formData = new FormData(form);

        // Add additional data
        formData.append("exercise_completed", allCorrect);
        formData.append("current_lesson_progress", current_lesson_progress);

        fetch(form.action || window.location.href, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest", // Mark as AJAX request
            },
        });
    }

    // Show answer
    showAnswerBtn.addEventListener("click", function () {
        blankInputs.forEach((input) => {
            const correctAnswer = input.getAttribute("data-answer");
            input.value = correctAnswer;
            input.classList.remove("incorrect");
            input.classList.add("correct");
        });

        // Update check button to show success
        checkBtn.style.background = "rgba(76, 175, 80, 0.2)";
        checkBtn.style.borderColor = "#4caf50";
        checkBtn.style.color = "#4caf50";
        checkBtn.textContent = "Perfect!";

        // Show the next button
        const nextBtn =
            document.getElementById("next-exercise-btn") ||
            document.getElementById("complete-lesson-btn");
        if (nextBtn) {
            nextBtn.style.display = "inline-block";
            nextBtn.style.opacity = "0";
            nextBtn.style.transition = "opacity 0.5s ease-in-out";
            setTimeout(() => {
                nextBtn.style.opacity = "1";
            }, 100);
        }
    });

    // Reset
    resetBtn.addEventListener("click", function (event) {
        event.preventDefault();

        blankInputs.forEach((input) => {
            // Clear the input value
            input.value = "";

            // Remove all state classes
            input.classList.remove("correct", "incorrect");

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

        // Hide the next button when resetting
        const nextBtn =
            document.getElementById("next-exercise-btn") ||
            document.getElementById("complete-lesson-btn");
        if (nextBtn) {
            nextBtn.style.display = "none";
        }
    });

    // Clear states when user starts typing again
    blankInputs.forEach((input) => {
        input.addEventListener("input", function () {
            this.classList.remove("correct", "incorrect");

            // Hide next button when user starts typing again
            const nextBtn =
                document.getElementById("next-exercise-btn") ||
                document.getElementById("complete-lesson-btn");
            if (nextBtn) {
                nextBtn.style.display = "none";
            }
        });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            // event.preventDefault();
            if (checkBtn && !checkBtn.disabled) {
                checkBtn.click();
            }
            return;
        }

        if (event.key === "Delete") {
            event.preventDefault();
            if (resetBtn && !resetBtn.disabled) {
                resetBtn.click();
            }
            return;
        }
    });

    // Enter key navigation
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
