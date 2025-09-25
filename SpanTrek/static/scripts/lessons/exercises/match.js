document.addEventListener("DOMContentLoaded", function () {
    const matchItems = document.querySelectorAll(".match-item");

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

    // Keyboard navigation - map number keys to match items based on their labels
    document.addEventListener("keydown", function (event) {
        const key = event.key;
        const keyNumber = parseInt(key); // Convert "1", "2", "3", "4" to 1, 2, 3, 4

        if (
            !isNaN(keyNumber) &&
            keyNumber >= 1 &&
            keyNumber <= matchItems.length
        ) {
            event.preventDefault();

            // Find the item with the matching data-choice label
            const targetItem = Array.from(matchItems).find(
                (item) =>
                    item.getAttribute("data-choice") === keyNumber.toString()
            );

            if (targetItem && !targetItem.classList.contains("matched")) {
                handleItemClick({ currentTarget: targetItem });
            }
        }
    });
});
