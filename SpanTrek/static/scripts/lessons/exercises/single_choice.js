document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.querySelector(".check-btn-single");
    const resetBtn = document.querySelector(".reset-btn-single");
    const choiceItems = document.querySelectorAll(".choice-item");

    let selectedChoice = null; // Only one choice can be selected
    let isAnswered = false;

    // Determine correct answers based on content
    const correctAnswers = new Set();

    choiceItems.forEach((item, index) => {
        const content = item
            .querySelector(".choice-content")
            .textContent.trim();

        // Check if content is all uppercase (indicating correct answer)
        const isAllUppercase =
            content === content.toUpperCase() &&
            content.length > 1 &&
            /[A-Z]/.test(content);

        if (isAllUppercase) {
            correctAnswers.add(index);
            // Convert to normal case for display
            item.querySelector(".choice-content").textContent =
                content.charAt(0).toUpperCase() +
                content.slice(1).toLowerCase();
        }
    });

    // If no correct answers found using above methods, fall back to last item
    if (correctAnswers.size === 0) {
        correctAnswers.add(choiceItems.length - 1);
    }

    // Initialize choice functionality
    choiceItems.forEach((item, index) => {
        item.addEventListener("click", () => handleChoiceClick(item, index));

        // Add choice labels (1, 2, 3, etc.)
        const label = (index + 1).toString();
        item.setAttribute("data-choice", label);
    });

    // Handle choice selection (single choice only)
    function handleChoiceClick(item, index) {
        // Don't allow clicking if already answered
        if (isAnswered) return;

        // If the same item is clicked, deselect it
        if (selectedChoice === index) {
            selectedChoice = null;
            item.classList.remove("selected");
            return;
        }

        // Deselect previous choice if any
        if (selectedChoice !== null) {
            choiceItems[selectedChoice].classList.remove("selected");
        }

        // Select the new choice
        selectedChoice = index;
        item.classList.add("selected");
    }

    // Check answer functionality
    checkBtn.addEventListener("click", function () {
        if (isAnswered) return;

        // Don't check if no choice is selected
        if (selectedChoice === null) return;

        isAnswered = true;

        // Mark all choices as disabled
        choiceItems.forEach((choice) => {
            choice.classList.add("disabled");
        });

        // Check if selected answer is correct
        const isCorrect = correctAnswers.has(selectedChoice);

        // Mark each choice based on the result
        choiceItems.forEach((item, index) => {
            item.classList.remove("selected");

            if (isCorrect && correctAnswers.has(index)) {
                // Only show correct answer if user got it right
                item.classList.add("correct");
            } else if (index === selectedChoice) {
                // Mark the selected choice as incorrect if it's wrong
                if (isCorrect) {
                    item.classList.add("correct");
                } else {
                    item.classList.add("incorrect");
                }
            }
        });

        if (isCorrect) {
            // Correct answer selected
            checkBtn.style.background = "rgba(76, 175, 80, 0.2)";
            checkBtn.style.borderColor = "#4caf50";
            checkBtn.style.color = "#4caf50";
            checkBtn.textContent = "Perfect!";
        } else {
            checkBtn.style.background = "rgba(244, 67, 54, 0.2)";
            checkBtn.style.borderColor = "#f44336";
            checkBtn.style.color = "#f44336";
            checkBtn.textContent = "Try again";
        }
    });

    // Reset functionality
    resetBtn.addEventListener("click", function () {
        // Reset all states
        isAnswered = false;
        selectedChoice = null;

        // Remove all classes from choices
        choiceItems.forEach((item) => {
            item.classList.remove(
                "selected",
                "correct",
                "incorrect",
                "disabled"
            );

            // Add brief highlight effect to show reset
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
    });

    // Keyboard navigation
    document.addEventListener("keydown", function (event) {
        // Handle Enter key for check button
        if (event.key === "Enter") {
            event.preventDefault();
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

        if (isAnswered) return;

        const key = event.key;
        const keyNumber = parseInt(key); // Convert "1", "2", "3", "4" to 1, 2, 3, 4
        const index = keyNumber - 1; // Convert to 0-based index (1→0, 2→1, 3→2, etc.)

        if (
            !isNaN(keyNumber) &&
            keyNumber >= 1 &&
            keyNumber <= choiceItems.length
        ) {
            event.preventDefault();
            handleChoiceClick(choiceItems[index], index);
        }
    });
});
