document.addEventListener("DOMContentLoaded", function () {
    // Tooltip element
    const tooltip = document.createElement("div");
    tooltip.className = "country-tooltip";
    document.body.appendChild(tooltip);

    const spanishCountries = document.querySelectorAll(".spanish-country");
    const lessonsDoneCountries = document.querySelectorAll(".lessons-done");
    const lockedCountries = document.querySelectorAll(".lessons-locked");

    const allCountries = [...spanishCountries, ...lessonsDoneCountries, ...lockedCountries];

    allCountries.forEach((country) => {
        country.addEventListener("mousemove", showTooltip);
        country.addEventListener("mouseleave", hideTooltip);
    });

    // Show tooltip
    function showTooltip(e) {
        const country = e.target;
        const countryData = JSON.parse(country.getAttribute("data-lessons"));
        const isStartingCountry =
            country.classList.contains("starting-country");
        const isLocked = country.classList.contains("lessons-locked");
        
        // Check if country is locked
        if (isLocked) {
            const lockedRequirements = {
                "Spain": "Poland",
                "Mexico": "Spain", 
                "Peru": "Mexico"
            };
            
            const requiredCountry = lockedRequirements[countryData.name];
            tooltip.innerHTML = `
                <strong style="color: #ff8c00">${countryData.name}</strong><br>
                <span style="color: #f44336">🔒 Country locked.<br> Finish all lessons in ${requiredCountry}.</span>
            `;
        } else {
            const country_lessons_available =
                countries_lessons_dict[countryData.name.toLowerCase()] || 0;
            const user_completed_lessons =
                user_countries_progress[countryData.name.toLowerCase()] || 0;

            // Completion percentage
            const percentage = country_lessons_available
                ? Math.round(
                      (user_completed_lessons / country_lessons_available) * 100
                  )
                : 0;

            // Tooltip content
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
        }

        // Position tooltip
        const rect = country.getBoundingClientRect();
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const scrollLeft =
            window.scrollX || document.documentElement.scrollLeft;

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
