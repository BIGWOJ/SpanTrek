// World Map Interactive Functionality
document.addEventListener("DOMContentLoaded", function () {
    const spanishCountries = document.querySelectorAll(".spanish-country");
    const countryInfo = document.getElementById("country-info");
    const countryName = document.getElementById("country-name");
    const countryCapital = document.getElementById("country-capital");
    const countryPopulation = document.getElementById("country-population");
    const closeBtn = document.getElementById("close-info");
    const exploreBtn = document.getElementById("explore-btn");

    let selectedCountry = null;

    // Remove the old createWorldBackground function since we now have proper country paths

    // Country information data
    const countryData = {
        Spain: {
            lessons: [
                "Basic Greetings",
                "Spanish Pronunciation",
                "European Spanish Culture",
            ],
            flag: "🇪🇸",
        },
        Mexico: {
            lessons: ["Mexican Spanish", "Day of the Dead", "Mexican Cuisine"],
            flag: "🇲🇽",
        },
        Argentina: {
            lessons: ["Tango Culture", "Argentine Spanish", "Buenos Aires"],
            flag: "🇦🇷",
        },
        Colombia: {
            lessons: ["Colombian Coffee", "Salsa Dancing", "Bogotá Dialect"],
            flag: "🇨🇴",
        },
        Chile: {
            lessons: ["Chilean Spanish", "Andes Mountains", "Santiago Culture"],
            flag: "🇨🇱",
        },
        Peru: {
            lessons: ["Machu Picchu", "Peruvian Cuisine", "Quechua Influence"],
            flag: "🇵🇪",
        },
        Venezuela: {
            lessons: ["Venezuelan Spanish", "Arepa Culture", "Caracas Life"],
            flag: "🇻🇪",
        },
        Ecuador: {
            lessons: [
                "Galápagos Islands",
                "Ecuadorian Spanish",
                "Quito Culture",
            ],
            flag: "🇪🇨",
        },
        Guatemala: {
            lessons: [
                "Mayan Heritage",
                "Guatemalan Spanish",
                "Traditional Textiles",
            ],
            flag: "🇬🇹",
        },
        Cuba: {
            lessons: ["Cuban Music", "Havana Culture", "Cuban Spanish"],
            flag: "🇨🇺",
        },
        Bolivia: {
            lessons: ["Bolivian Spanish", "Altiplano Culture", "La Paz Life"],
            flag: "🇧🇴",
        },
        "Dominican Republic": {
            lessons: [
                "Merengue Dance",
                "Dominican Spanish",
                "Caribbean Culture",
            ],
            flag: "🇩🇴",
        },
        Honduras: {
            lessons: [
                "Honduran Spanish",
                "Maya Ruins",
                "Central American Culture",
            ],
            flag: "🇭🇳",
        },
        Paraguay: {
            lessons: [
                "Guaraní Language",
                "Paraguayan Spanish",
                "Asunción Culture",
            ],
            flag: "🇵🇾",
        },
        Nicaragua: {
            lessons: [
                "Nicaraguan Spanish",
                "Colonial Cities",
                "Lake Nicaragua",
            ],
            flag: "🇳🇮",
        },
        "El Salvador": {
            lessons: ["Salvadoran Spanish", "Pupusa Culture", "San Salvador"],
            flag: "🇸🇻",
        },
        "Costa Rica": {
            lessons: ["Costa Rican Spanish", "Pura Vida", "Biodiversity"],
            flag: "🇨🇷",
        },
        Panama: {
            lessons: ["Panamanian Spanish", "Canal Culture", "Panama City"],
            flag: "🇵🇦",
        },
        Uruguay: {
            lessons: [
                "Uruguayan Spanish",
                "Montevideo Culture",
                "Tango Heritage",
            ],
            flag: "🇺🇾",
        },
        "Puerto Rico": {
            lessons: [
                "Puerto Rican Spanish",
                "Salsa Music",
                "San Juan Culture",
            ],
            flag: "🇵🇷",
        },
        "Equatorial Guinea": {
            lessons: ["African Spanish", "Malabo Culture", "Unique Dialect"],
            flag: "🇬🇶",
        },
    };

    // Add hover effects and click handlers
    spanishCountries.forEach((country) => {
        // Hover effects
        country.addEventListener("mouseenter", function () {
            if (this !== selectedCountry) {
                this.style.transform = "scale(1.02)";
                this.style.filter =
                    "drop-shadow(0 4px 8px rgba(255, 165, 31, 0.6))";
            }
        });

        country.addEventListener("mouseleave", function () {
            if (this !== selectedCountry) {
                this.style.transform = "scale(1)";
                this.style.filter = "none";
            }
        });

        // Click handler
        country.addEventListener("click", function () {
            selectCountry(this);
        });
    });

    // Select country function
    function selectCountry(countryElement) {
        // Remove active class from previous selection
        if (selectedCountry) {
            selectedCountry.classList.remove("active");
        }

        // Set new selection
        selectedCountry = countryElement;
        countryElement.classList.add("active");

        // Get country data
        const country = countryElement.dataset.country;
        const capital = countryElement.dataset.capital;
        const population = countryElement.dataset.population;
        const data = countryData[country];

        // Update info panel
        countryName.textContent = `${data?.flag || "🌎"} ${country}`;
        countryCapital.textContent = capital;
        countryPopulation.textContent = population;

        // Show info panel
        countryInfo.classList.add("active");

        // Update explore button
        exploreBtn.onclick = function () {
            exploreCountry(country, data);
        };
    }

    // Explore country function
    function exploreCountry(country, data) {
        alert(
            `Exploring ${country}!\n\nAvailable lessons:\n${
                data?.lessons?.join("\n") || "Coming soon!"
            }`
        );
        // Here you would redirect to the actual lessons page
        // window.location.href = `/lessons/${country.toLowerCase().replace(/\s+/g, '-')}/`;
    }

    // Close info panel
    closeBtn.addEventListener("click", function () {
        countryInfo.classList.remove("active");
        if (selectedCountry) {
            selectedCountry.classList.remove("active");
            selectedCountry = null;
        }
    });

    // Animation for country paths on load
    function animateCountries() {
        spanishCountries.forEach((country, index) => {
            setTimeout(() => {
                country.style.opacity = "0";
                country.style.transform = "scale(0.8)";

                setTimeout(() => {
                    country.style.transition = "all 0.5s ease";
                    country.style.opacity = "0.8";
                    country.style.transform = "scale(1)";
                }, index * 100);
            }, 500);
        });
    }

    // Start animations
    animateCountries();

    // Add floating animation to some countries
    function addFloatingAnimation() {
        const floatingCountries = spanishCountries;

        floatingCountries.forEach((country, index) => {
            if (country && index < 4) {
                // Only animate first 4 countries
                country.style.animation = `float 3s ease-in-out infinite ${
                    index * 0.5
                }s`;
            }
        });
    }

    // Add CSS for floating animation
    const style = document.createElement("style");
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translateY(0px) scale(1); }
            50% { transform: translateY(-3px) scale(1.05); }
        }
    `;
    document.head.appendChild(style);

    // Start floating animation after initial load
    setTimeout(addFloatingAnimation, 2000);

    // Add welcome message
    setTimeout(() => {
        if (!selectedCountry) {
            countryName.textContent = "¡Bienvenidos! Welcome!";
            countryCapital.textContent = "Click any country to explore";
            countryPopulation.textContent = "Start your Spanish journey";
            countryInfo.classList.add("active");

            // Auto-hide after 3 seconds
            setTimeout(() => {
                if (countryName.textContent.includes("Bienvenidos")) {
                    countryInfo.classList.remove("active");
                }
            }, 3000);
        }
    }, 3000);
});
