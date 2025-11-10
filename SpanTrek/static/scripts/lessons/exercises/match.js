document.addEventListener("DOMContentLoaded", function () {
    const matchItems = document.querySelectorAll(".match-item");
    const showAnswerBtn = document.querySelector(".show-answer-btn-match");

    let selectedItems = [];
    let matches = [];

    // Initialize match functionality and add choice labels
    matchItems.forEach((item, index) => {
        item.addEventListener("click", handleItemClick);

        // Add choice labels based on actual DOM structure:
        const totalItems = matchItems.length;
        const itemsPerColumn = totalItems / 2;

        let label;
        if (index < itemsPerColumn) {
            // Left column items: indices 0 to itemsPerColumn-1
            label = (index * 2 + 1).toString();
        } else {
            // Right column items: indices itemsPerColumn to totalItems-1
            const rightColumnPosition = index - itemsPerColumn;
            label = ((rightColumnPosition + 1) * 2).toString();
        }

        item.setAttribute("data-choice", label);
    });

    // Handle item selection and matching
    function handleItemClick(event) {
        const item = event.currentTarget;

        // Don't allow clicking on already matched items
        if (item.classList.contains("matched")) {
            return;
        }

        // Hide next button when user starts making new selections
        const nextBtn =
            document.getElementById("next-exercise-btn") ||
            document.getElementById("complete-lesson-btn");
        if (nextBtn && selectedItems.length === 0) {
            // Only hide on first selection to avoid hiding during matching process
            nextBtn.style.display = "none";
        }

        // Remove any previous incorrect styling
        item.classList.remove("incorrect");

        // If item is already selected, deselect it
        if (item.classList.contains("selected")) {
            item.classList.remove("selected");
            selectedItems = selectedItems.filter(
                (selected) => selected !== item
            );
            return;
        }

        // If we already have 2 items selected, deselect all
        if (selectedItems.length >= 2) {
            selectedItems.forEach((selected) =>
                selected.classList.remove("selected")
            );
            selectedItems = [];
        }

        // Select the clicked item
        item.classList.add("selected");
        selectedItems.push(item);

        // If we have 2 items selected, check if they match
        if (selectedItems.length === 2) {
            setTimeout(() => {
                checkMatch();
            }, 300);
        }
    }

    // Check if two selected items match
    function checkMatch() {
        if (selectedItems.length !== 2) return;

        const [item1, item2] = selectedItems;
        const match1 = item1.getAttribute("data-match");
        const match2 = item2.getAttribute("data-match");

        if (match1 === match2) {
            // Items match
            item1.classList.remove("selected");
            item2.classList.remove("selected");
            item1.classList.add("matched");
            item2.classList.add("matched");

            // Store the match
            matches.push({ item1, item2, correct: true });

            // Check if all items are matched
            const allMatched = Array.from(matchItems).every((item) =>
                item.classList.contains("matched")
            );

            if (allMatched) {
                // Show the next button when all matches are completed
                const nextBtn =
                    document.getElementById("next-exercise-btn") ||
                    document.getElementById("complete-lesson-btn");
                if (nextBtn) {
                    nextBtn.style.display = "inline-block";
                    nextBtn.style.opacity = "0";
                    nextBtn.style.transition = "opacity 0.5s ease-in-out";
                    setTimeout(() => {
                        nextBtn.style.opacity = "1";
                    }, 500);
                }
            }
        } else {
            // Items don't match - show briefly then deselect
            item1.classList.add("incorrect");
            item2.classList.add("incorrect");

            setTimeout(() => {
                item1.classList.remove("selected", "incorrect");
                item2.classList.remove("selected", "incorrect");
            }, 800);
        }

        selectedItems = [];
    }

    // Show answer functionality
    showAnswerBtn.addEventListener("click", function () {
        // Clear any selections
        selectedItems.forEach((item) => item.classList.remove("selected"));
        selectedItems = [];

        // Match all items automatically
        matchItems.forEach((item) => {
            item.classList.remove("selected", "incorrect");
            item.classList.add("matched");
        });

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

    // Keyboard navigation - NUMPAD ONLY - map numpad number keys to match items based on their labels
    document.addEventListener("keydown", function (event) {
        const code = event.code;

        // Handle ONLY numpad numbers (1, 2, 3, etc.) - numpad navigation only
        if (code.startsWith("Numpad") && event.key >= "1" && event.key <= "9") {
            const keyNumber = parseInt(event.key);

            if (keyNumber >= 1 && keyNumber <= matchItems.length) {
                event.preventDefault();

                // Find the item with the matching data-choice label
                const targetItem = Array.from(matchItems).find(
                    (item) =>
                        item.getAttribute("data-choice") ===
                        keyNumber.toString()
                );

                if (targetItem && !targetItem.classList.contains("matched")) {
                    handleItemClick({ currentTarget: targetItem });
                }
            }
            return;
        }
    });
});
