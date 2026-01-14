// Calendar functionality
class ActivityCalendar {
    constructor() {
        this.currentDate = new Date();
        this.today = new Date();
        this.activeDays = window.userActivityDays || [];
        this.init();
    }

    init() {
        this.renderCalendar();
        this.bindEvents();
    }

    bindEvents() {
        document.getElementById("prev-month")?.addEventListener("click", () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.renderCalendar();
        });

        document.getElementById("next-month")?.addEventListener("click", () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.renderCalendar();
        });
    }

    renderCalendar() {
        const monthNames = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ];

        const currentMonth = document.getElementById("current-month");
        if (currentMonth) {
            currentMonth.textContent = `${
                monthNames[this.currentDate.getMonth()]
            } ${this.currentDate.getFullYear()}`;
        }

        const calendarGrid = document.getElementById("calendar-grid");
        if (!calendarGrid) return;

        calendarGrid.innerHTML = "";

        // Day headers
        const dayHeaders = ["M", "T", "W", "T", "F", "S", "S"];
        dayHeaders.forEach((day) => {
            const dayHeader = document.createElement("div");
            dayHeader.className = "calendar-day-header";
            dayHeader.textContent = day;
            dayHeader.style.fontWeight = "bold";
            dayHeader.style.color = "#666";
            dayHeader.style.fontSize = "0.8rem";
            dayHeader.style.textAlign = "center";
            calendarGrid.appendChild(dayHeader);
        });

        // Get first day of month and number of days
        const firstDay = new Date(
            this.currentDate.getFullYear(),
            this.currentDate.getMonth(),
            1
        );
        const lastDay = new Date(
            this.currentDate.getFullYear(),
            this.currentDate.getMonth() + 1,
            0
        );
        const startDate = (firstDay.getDay() + 6) % 7;
        const daysInMonth = lastDay.getDate();

        // Add empty cells for days before month starts
        for (let i = 0; i < startDate; i++) {
            const emptyDay = document.createElement("div");
            emptyDay.className = "calendar-day other-month";
            calendarGrid.appendChild(emptyDay);
        }

        // Add days of current month
        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement("div");
            dayElement.className = "calendar-day";
            dayElement.textContent = day;

            // Check if this day is today
            const dayDate = new Date(
                this.currentDate.getFullYear(),
                this.currentDate.getMonth(),
                day
            );
            if (this.isSameDay(dayDate, this.today)) {
                dayElement.classList.add("today");
            }

            const dayDateISO = this.formatDateToISO(dayDate);
            if (this.activeDays.includes(dayDateISO)) {
                dayElement.classList.add("active");
                dayElement.title = "Completed lesson this day";
            }

            calendarGrid.appendChild(dayElement);
        }
    }

    isSameDay(date1, date2) {
        return (
            date1.getDate() === date2.getDate() &&
            date1.getMonth() === date2.getMonth() &&
            date1.getFullYear() === date2.getFullYear()
        );
    }

    formatDateToISO(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        return `${year}-${month}-${day}`;
    }
}

// Expand settings section
function expandSettings() {
    const collapsedDiv = document.getElementById("settings-collapsed");
    const expandedDiv = document.getElementById("settings-expanded");

    collapsedDiv.style.display = "none";

    expandedDiv.style.display = "block";
    expandedDiv.style.opacity = "0";
    expandedDiv.style.transform = "translateY(20px)";

    expandedDiv.offsetHeight;

    expandedDiv.style.transition = "opacity 0.4s ease, transform 0.4s ease";
    expandedDiv.style.opacity = "1";
    expandedDiv.style.transform = "translateY(0)";
}

// Collapse settings section
function collapseSettings() {
    const collapsedDiv = document.getElementById("settings-collapsed");
    const expandedDiv = document.getElementById("settings-expanded");

    expandedDiv.style.transition = "opacity 0.4s ease, transform 0.4s ease";
    expandedDiv.style.opacity = "0";
    expandedDiv.style.transform = "translateY(-20px)";

    setTimeout(() => {
        expandedDiv.style.display = "none";
        collapsedDiv.style.display = "flex";

        expandedDiv.style.transform = "";
        expandedDiv.style.opacity = "";
        expandedDiv.style.transition = "";
    }, 400);

    const form = document.querySelector(".profile-form");
}

// Stats animation
function animateStats() {
    const statValues = document.querySelectorAll(".stat-value");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = parseInt(target.textContent) || 0;
                animateValue(target, 0, finalValue, 1000);
            }
        });
    });

    statValues.forEach((stat) => observer.observe(stat));
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const currentValue = Math.floor(progress * (end - start) + start);

        if (element.textContent.includes("%")) {
            element.textContent = currentValue + "%";
        } else {
            element.textContent = currentValue;
        }

        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Achievement hover effects
function initAchievements() {
    const achievementCards = document.querySelectorAll(".achievement-card");

    achievementCards.forEach((card) => {
        card.addEventListener("mouseenter", () => {
            const badge = card.querySelector(".achievement-badge");
            if (card.classList.contains("earned")) {
                badge.style.transform = "scale(1.2) rotate(10deg)";
                badge.style.transition = "transform 0.3s ease";
            }
        });

        card.addEventListener("mouseleave", () => {
            const badge = card.querySelector(".achievement-badge");
            badge.style.transform = "scale(1) rotate(0deg)";
        });
    });
}

// Progress bar animation
function animateProgressBars() {
    const progressBars = document.querySelectorAll(".progress-fill");
    progressBars.forEach((bar) => {
        const targetWidth = bar.style.width;

        bar.style.width = "0%";
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 500);
    });
}

// Avatar upload functionality
function initAvatarUpload() {
    const avatarInput = document.getElementById("avatar-input");
    const avatarPreview = document.getElementById("avatar-preview");

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener("change", function (e) {
            const file = e.target.files[0];

            if (file) {
                // Preview
                const reader = new FileReader();
                reader.onload = function (e) {
                    avatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });

        // Drag and drop
        const uploadContainer = document.querySelector(
            ".profile-picture-section"
        );
        if (uploadContainer) {
            uploadContainer.addEventListener("dragover", function (e) {
                e.preventDefault();
                uploadContainer.style.borderColor = "#ffa51f";
                uploadContainer.style.background = "rgba(255, 165, 31, 0.1)";
            });

            uploadContainer.addEventListener("dragleave", function (e) {
                e.preventDefault();
                uploadContainer.style.borderColor = "#ddd";
                uploadContainer.style.background = "rgba(255, 165, 31, 0.02)";
            });

            uploadContainer.addEventListener("drop", function (e) {
                e.preventDefault();
                uploadContainer.style.borderColor = "#ddd";
                uploadContainer.style.background = "rgba(255, 165, 31, 0.02)";

                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    avatarInput.files = files;
                    avatarInput.dispatchEvent(new Event("change"));
                }
            });
        }
    }
}

// Initialize all functionality when page loads
document.addEventListener("DOMContentLoaded", () => {
    new ActivityCalendar();

    animateStats();
    animateProgressBars();
    initAchievements();
    initAvatarUpload();
});
