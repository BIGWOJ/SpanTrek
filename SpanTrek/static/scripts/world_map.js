document.addEventListener("DOMContentLoaded", function () {
    // Create tooltip element
    const tooltip = document.createElement("div");
    tooltip.className = "country-tooltip";
    document.body.appendChild(tooltip);

    // Get all Spanish country elements
    const spanishCountries = document.querySelectorAll(".spanish-country");

    // Add event listeners to each country
    spanishCountries.forEach((country) => {
        country.addEventListener("mousemove", showTooltip);
        country.addEventListener("mouseleave", hideTooltip);
    });

    // Show tooltip function
    function showTooltip(e) {
        const country = e.target;
        const countryData = JSON.parse(
            country.dataset.lessons ||
                '{"completed": 0, "total": 0, "name": "Unknown"}'
        );

        // Calculate completion percentage
        const percentage =
            countryData.total > 0
                ? Math.round((countryData.completed / countryData.total) * 100)
                : 0;

        // Update tooltip content
        tooltip.innerHTML = `
            <strong style="color: #ff8c00">${countryData.name}</strong><br>
            Progress: ${percentage}%<br>
            Completed: ${countryData.completed}/${countryData.total} lessons
        `;

        // Position tooltip
        const rect = country.getBoundingClientRect();
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const scrollLeft =
            window.scrollX || document.documentElement.scrollLeft;

        // Calculate position 20 pixels above the country's top edge
        const tooltipX = rect.left + rect.width / 2 + scrollLeft;
        const tooltipY = rect.top + scrollTop - 20;

        tooltip.style.left = `${tooltipX}px`;
        tooltip.style.top = `${tooltipY}px`;
        tooltip.classList.add("visible");
    }

    // Hide tooltip function
    function hideTooltip() {
        tooltip.classList.remove("visible");
    }
});
