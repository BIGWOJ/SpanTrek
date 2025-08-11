// User Page JavaScript Functionality

// Calendar functionality
class ActivityCalendar {
    constructor() {
        this.currentDate = new Date();
        this.today = new Date();
        this.activeDays = [1, 3, 5, 8, 10, 11]; // Example active days for current month
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

        // Add day headers
        const dayHeaders = ["S", "M", "T", "W", "T", "F", "S"];
        dayHeaders.forEach((day) => {
            const dayHeader = document.createElement("div");
            dayHeader.className = "calendar-day-header";
            dayHeader.textContent = day;
            dayHeader.style.fontWeight = "bold";
            dayHeader.style.color = "#666";
            dayHeader.style.fontSize = "0.8rem";
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
        const startDate = firstDay.getDay();
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

            // Check if this day has activity
            if (
                this.activeDays.includes(day) &&
                this.currentDate.getMonth() === this.today.getMonth()
            ) {
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
}

// Settings functionality
function toggleEdit(section) {
    const content = document.getElementById(`${section}-content`);
    const editBtn = content.parentElement.querySelector(".edit-btn");

    if (editBtn.textContent === "Edit") {
        enterEditMode(content, editBtn);
    } else {
        saveChanges(content, editBtn);
    }
}

function enterEditMode(content, button) {
    button.textContent = "Save";
    button.style.background = "#28a745";

    const rows = content.querySelectorAll(".info-row");
    rows.forEach((row) => {
        const span = row.querySelector("span");
        if (span && !row.querySelector("input")) {
            const currentValue = span.textContent;
            const input = document.createElement("input");
            input.type = "text";
            input.value = currentValue;
            input.style.border = "1px solid #ddd";
            input.style.padding = "5px";
            input.style.borderRadius = "4px";
            input.style.background = "#fff";
            input.style.color = "#1a1a1a";

            span.replaceWith(input);
        }
    });
}

function saveChanges(content, button) {
    button.textContent = "Edit";
    button.style.background = "#ffa51f";

    const rows = content.querySelectorAll(".info-row");
    rows.forEach((row) => {
        const input = row.querySelector("input");
        if (input) {
            const span = document.createElement("span");
            span.textContent = input.value;
            span.style.color = "#1a1a1a";
            span.style.fontWeight = "500";

            input.replaceWith(span);
        }
    });

    // Show success message
    showNotification("Settings saved successfully!", "success");
}

// Notification system
function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Style the notification
    Object.assign(notification.style, {
        position: "fixed",
        top: "20px",
        right: "20px",
        padding: "15px 20px",
        borderRadius: "8px",
        color: "#fff",
        fontWeight: "bold",
        zIndex: "9999",
        transform: "translateX(100%)",
        transition: "transform 0.3s ease",
        minWidth: "250px",
        textAlign: "center",
    });

    // Set background color based on type
    switch (type) {
        case "success":
            notification.style.background = "#28a745";
            break;
        case "error":
            notification.style.background = "#dc3545";
            break;
        case "warning":
            notification.style.background = "#ffc107";
            notification.style.color = "#1a1a1a";
            break;
        default:
            notification.style.background = "#ffa51f";
    }

    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = "translateX(0)";
    }, 100);

    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = "translateX(100%)";
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
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

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = "0%";
                progressBar.style.transition = "width 1.5s ease-in-out";

                setTimeout(() => {
                    progressBar.style.width = width;
                }, 100);
            }
        });
    });

    progressBars.forEach((bar) => observer.observe(bar));
}

// Toggle switch functionality
function initToggleSwitches() {
    const toggleSwitches = document.querySelectorAll(".toggle-switch input");

    toggleSwitches.forEach((toggle) => {
        toggle.addEventListener("change", (e) => {
            const setting = e.target.id.replace("-", " ");
            const status = e.target.checked ? "enabled" : "disabled";

            showNotification(
                `${
                    setting.charAt(0).toUpperCase() + setting.slice(1)
                } ${status}`,
                "info"
            );
        });
    });
}

// Keyboard shortcuts
function initKeyboardShortcuts() {
    document.addEventListener("keydown", (e) => {
        // Alt + H - Go to home
        if (e.altKey && e.key === "h") {
            e.preventDefault();
            window.location.href = "/";
        }

        // Alt + S - Focus on first settings input
        if (e.altKey && e.key === "s") {
            e.preventDefault();
            const firstInput = document.querySelector(".settings-card input");
            if (firstInput) {
                firstInput.focus();
            }
        }
    });
}

// Initialize all functionality when page loads
document.addEventListener("DOMContentLoaded", () => {
    // Initialize calendar
    new ActivityCalendar();

    // Initialize animations and interactions
    animateStats();
    animateProgressBars();
    initAchievements();
    initToggleSwitches();
    initKeyboardShortcuts();

    // Add loading effect to action buttons
    const actionButtons = document.querySelectorAll(".action-btn");
    actionButtons.forEach((btn) => {
        btn.addEventListener("click", (e) => {
            if (btn.href && !btn.href.includes("logout")) {
                btn.style.opacity = "0.7";
                btn.innerHTML = `<span class="btn-icon">⏳</span> Loading...`;
            }
        });
    });

    // Welcome message
    setTimeout(() => {
        showNotification("Welcome to your profile!", "info");
    }, 500);
});

// Export functions for potential external use
window.UserPageFunctions = {
    toggleEdit,
    showNotification,
    ActivityCalendar,
};
