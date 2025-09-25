document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.querySelector(".check-btn-multi");
    const resetBtn = document.querySelector(".reset-btn-multi");
    const choiceItems = document.querySelectorAll(".choice-item");

    let selectedChoices = new Set();
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

    // Initialize choice functionality
    choiceItems.forEach((item, index) => {
        item.addEventListener("click", () => handleChoiceClick(item, index));

        // Add choice labels (1, 2, 3, etc.)
        const label = (index + 1).toString(); // 1, 2, 3, 4...
        item.setAttribute("data-choice", label);
    });

    // Handle choice selection
    function handleChoiceClick(item, index) {
        // Don't allow clicking if already answered
        if (isAnswered) return;

        // Toggle selection for multiple choice
        if (selectedChoices.has(index)) {
            // Deselect
            selectedChoices.delete(index);
            item.classList.remove("selected");
        } else {
            // Select
            selectedChoices.add(index);
            item.classList.add("selected");
        }
    }

    // Check answer functionality
    checkBtn.addEventListener("click", function () {
        if (isAnswered) return;

        isAnswered = true;

        // Mark all choices as disabled
        choiceItems.forEach((choice) => {
            choice.classList.add("disabled");
        });

        // Check if selected answers match correct answers exactly
        const selectedArray = Array.from(selectedChoices);
        const correctArray = Array.from(correctAnswers);

        const isCorrect =
            selectedArray.length === correctArray.length &&
            selectedArray.every((index) => correctAnswers.has(index));

        // Mark each choice as correct or incorrect
        choiceItems.forEach((item, index) => {
            item.classList.remove("selected");

            if (correctAnswers.has(index)) {
                item.classList.add("correct");
            } else if (selectedChoices.has(index)) {
                item.classList.add("incorrect");
            }
        });

        if (isCorrect) {
            // All correct answers selected, no incorrect ones
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
        selectedChoices.clear();

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

        setTimeout(() => {
            resetBtn.textContent = "Reset";
            resetBtn.style.color = "";
        }, 1000);
    });

    // Keyboard navigation
    document.addEventListener("keydown", function (event) {
        // Handle Enter key for check button
        if (event.key === "Enter") {
            event.preventDefault();
            checkBtn.click();
            return;
        }

        // Handle Delete key for reset button
        if (event.key === "Delete") {
            event.preventDefault();
            resetBtn.click();
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
            handleChoiceClick(choiceItems[index], index);
        }
    });
});

