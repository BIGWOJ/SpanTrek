document.addEventListener("DOMContentLoaded", function () {
    // Keyboard navigation for Next button
    document.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.code === "NumpadEnter") {
            // Check if user is typing in an input field
            const activeElement = document.activeElement;
            const isInputField =
                activeElement.tagName === "INPUT" ||
                activeElement.tagName === "TEXTAREA";

            // Only trigger Next button if not in an input field to prevent skipping to next exercise instantly after answering
            if (!isInputField) {
                event.preventDefault();
                const nextBtn =
                    document.getElementById("next-exercise-btn") ||
                    document.getElementById("complete-lesson-btn");

                if (nextBtn && nextBtn.style.display !== "none") {
                    nextBtn.click();
                }
            }
        }
    });
});
