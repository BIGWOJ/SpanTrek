document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.querySelector(".check-btn");
    const resetBtn = document.querySelector(".reset-btn");
    const blankInputs = document.querySelectorAll(".blank-input");

    // Check answers functionality
    checkBtn.addEventListener("click", function () {
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
    });

    // Optional: Clear states when user starts typing again
    blankInputs.forEach((input) => {
        input.addEventListener("input", function () {
            this.classList.remove("correct", "incorrect");
        });
    });
});
