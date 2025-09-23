document.addEventListener("DOMContentLoaded", function () {
    // Create tooltip element
    const tooltip = document.createElement("div");
    tooltip.className = "country-tooltip";
    document.body.appendChild(tooltip);

    const spanishCountries = document.querySelectorAll(".spanish-country");
    const lessonsDoneCountries = document.querySelectorAll(".lessons-done");

    const allCountries = [...spanishCountries, ...lessonsDoneCountries];

    // Add event listeners to each country
    allCountries.forEach((country) => {
        country.addEventListener("mousemove", showTooltip);
        country.addEventListener("mouseleave", hideTooltip);
    });

    // Show tooltip function
    function showTooltip(e) {
        const country = e.target;
        const countryData = JSON.parse(country.getAttribute("data-lessons"));
        const isStartingCountry =
            country.classList.contains("starting-country");
        
        const country_lessons_available =
            countries_lessons_dict[countryData.name.toLowerCase()] || 0;
        const user_completed_lessons =
            user_countries_progress[countryData.name.toLowerCase()] || 0;

        // Calculate completion percentage
        const percentage = country_lessons_available
            ? Math.round(
                  (user_completed_lessons / country_lessons_available) * 100
              )
            : 0;

        // Set tooltip content
        if (isStartingCountry) {
            tooltip.innerHTML = `
                <strong style="color: #ff8c00">Poland</strong><br>
                <span style="color: #4CAF50">Start your journey here!</span><br>
                Progress: ${percentage}%<br>
                Completed: ${user_completed_lessons}/${country_lessons_available} lessons
            `;
        } else {
            tooltip.innerHTML = `
                <strong style="color: #ff8c00">${countryData.name}</strong><br>
                Progress: ${percentage}%<br>
                Completed: ${user_completed_lessons}/${country_lessons_available} lessons
            `;
        }

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
