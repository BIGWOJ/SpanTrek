document.addEventListener("DOMContentLoaded", function () {
    const checkBtn = document.querySelector(".check-btn");
    const resetBtn = document.querySelector(".reset-btn");
    const matchItems = document.querySelectorAll(".match-item");
    const connectionSvg = document.querySelector(".connection-svg");

    let selectedItems = [];
    let matches = [];

    // Initialize match functionality
    matchItems.forEach((item) => {
        item.addEventListener("click", handleItemClick);
    });

    // Handle item selection and matching
    function handleItemClick(event) {
        const item = event.currentTarget;

        // Don't allow clicking on already matched items
        if (item.classList.contains("matched")) {
            return;
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

    // Check answers functionality
    checkBtn.addEventListener("click", function () {
        let allCorrect = true;
        let checkedMatches = [];

        // Clear previous connection lines
        connectionSvg.innerHTML = "";

        // Check all current matches
        matches.forEach((match) => {
            const { item1, item2 } = match;
            const match1 = item1.getAttribute("data-match");
            const match2 = item2.getAttribute("data-match");
            const isCorrect = match1 === match2;

            if (!isCorrect) {
                allCorrect = false;
                item1.classList.add("incorrect");
                item2.classList.add("incorrect");
            }

            checkedMatches.push({ item1, item2, correct: isCorrect });
        });
    });
});
