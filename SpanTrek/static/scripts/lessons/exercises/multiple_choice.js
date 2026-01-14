document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.querySelector(".check-btn-multi");
    const resetBtn = document.querySelector(".reset-btn-multi");
    const showAnswerBtn = document.querySelector(".show-answer-btn-multi");
    const choiceItems = document.querySelectorAll(".choice-item");

    let selectedChoices = new Set();
    let isAnswered = false;

    // Determine correct answers
    const correctAnswers = new Set();

    choiceItems.forEach((item, index) => {
        // Get the original content before any template filters
        const originalContent = item.getAttribute("data-original").trim();

        // Check if original content is all uppercase (correct answer)
        const isAllUppercase =
            originalContent === originalContent.toUpperCase() &&
            originalContent.length > 1 &&
            /[A-Z]/.test(originalContent);

        if (isAllUppercase) {
            correctAnswers.add(index);
        }
    });

    choiceItems.forEach((item, index) => {
        item.addEventListener("click", () => handleChoiceClick(item, index));

        // Add choice labels
        const label = (index + 1).toString();
        item.setAttribute("data-choice", label);
    });

    // Choice selection
    function handleChoiceClick(item, index) {
        // Don't allow clicking if already answered
        if (isAnswered) return;

        // Hide next button when user starts making new selections
        const nextBtn =
            document.getElementById("next-exercise-btn") ||
            document.getElementById("complete-lesson-btn");
        if (nextBtn) {
            nextBtn.style.display = "none";
        }

        // Toggle selection for multiple choice
        if (selectedChoices.has(index)) {
            selectedChoices.delete(index);
            item.classList.remove("selected");
        } else {
            selectedChoices.add(index);
            item.classList.add("selected");
        }
    }

    // Check answer
    checkBtn.addEventListener("click", function () {
        if (isAnswered) return;

        // Don't check if no choices are selected
        if (selectedChoices.size === 0) return;

        isAnswered = true;

        // Mark all choices as disabled
        choiceItems.forEach((choice) => {
            choice.classList.add("disabled");
        });

        // Check if selected answers match correct answers
        const selectedArray = Array.from(selectedChoices);
        const correctArray = Array.from(correctAnswers);

        const isCorrect =
            selectedArray.length === correctArray.length &&
            selectedArray.length > 0 &&
            selectedArray.every((index) => correctAnswers.has(index));

        // Mark each choice based on the result
        choiceItems.forEach((item, index) => {
            item.classList.remove("selected");

            // Only show correct answers if user got them all right
            if (isCorrect && correctAnswers.has(index)) {
                item.classList.add("correct");
            } else if (selectedChoices.has(index)) {
                if (isCorrect) {
                    item.classList.add("correct");
                } else {
                    item.classList.add("incorrect");
                }
            }
        });

        if (isCorrect) {
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
                }, 100);
            }
        } else {
            checkBtn.style.background = "rgba(244, 67, 54, 0.2)";
            checkBtn.style.borderColor = "#f44336";
            checkBtn.style.color = "#f44336";
            checkBtn.textContent = "Try again";
        }
    });

    // Show answer
    showAnswerBtn.addEventListener("click", function () {
        // Mark as answered to prevent clicks
        isAnswered = true;

        // Clear any previous selections and mark correct answers
        choiceItems.forEach((item, index) => {
            item.classList.remove("selected", "incorrect");
            item.classList.add("disabled");

            if (correctAnswers.has(index)) {
                item.classList.add("correct");
                selectedChoices.add(index);
            }
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
    resetBtn.addEventListener("click", function () {
        // Reset all states
        isAnswered = false;
        selectedChoices.clear();

        // Remove all classes from choices
        choiceItems.forEach((item) => {
            item.classList.remove(
                "selected",
                "correct",
                "incorrect",
                "disabled"
            );

            item.style.transition = "all 0.3s ease";
            item.style.backgroundColor = "rgba(255, 165, 31, 0.2)";

            setTimeout(() => {
                item.style.backgroundColor = "";
            }, 300);
        });

        // Reset check button
        checkBtn.style.background = "";
        checkBtn.style.borderColor = "";
        checkBtn.style.color = "";
        checkBtn.textContent = "Check answer";

        // Hide the next button when resetting
        const nextBtn =
            document.getElementById("next-exercise-btn") ||
            document.getElementById("complete-lesson-btn");
        if (nextBtn) {
            nextBtn.style.display = "none";
        }

        setTimeout(() => {
            resetBtn.textContent = "Reset";
            resetBtn.style.color = "";
        }, 1000);

        setTimeout(() => {
            checkBtn.style.background = "";
            checkBtn.style.borderColor = "";
            checkBtn.style.color = "";
            checkBtn.textContent = "Check answer";
        }, 2000);
    });

    // Keyboard navigation
    document.addEventListener("keydown", function (event) {
        const code = event.code;

        if (event.key === "Enter") {
            event.preventDefault();
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

        if (isAnswered) return;

        // Numpad navigation for choices
        if (code.startsWith("Numpad") && event.key >= "1" && event.key <= "9") {
            const keyNumber = parseInt(event.key);
            const index = keyNumber - 1;

            if (keyNumber <= choiceItems.length) {
                event.preventDefault();
                handleChoiceClick(choiceItems[index], index);
            }
            return;
        }
    });
});
