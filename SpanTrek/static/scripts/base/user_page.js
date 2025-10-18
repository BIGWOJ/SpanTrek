// User Page JavaScript Functionality

// Calendar functionality
class ActivityCalendar {
    constructor() {
        this.currentDate = new Date();
        this.today = new Date();
        // Use actual activity days from Django model instead of hardcoded values
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

            // Check if this day has activity using DD-MM-YYYY date format
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

function expandSettings() {
    const collapsedDiv = document.getElementById("settings-collapsed");
    const expandedDiv = document.getElementById("settings-expanded");

    collapsedDiv.style.display = "none";
    expandedDiv.style.display = "block";
}

// Collapse settings section
function collapseSettings() {
    const collapsedDiv = document.getElementById("settings-collapsed");
    const expandedDiv = document.getElementById("settings-expanded");

    expandedDiv.style.display = "none";
    collapsedDiv.style.display = "flex";

    // Reset the form when collapsing
    const form = document.querySelector(".profile-form");
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
// To ensure compatibility with the calendar, store activity_days as strings in DD-MM-YYYY format: "DD-MM-YYYY" (e.g., "10-06-2024").
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
        // Get user experience from the XP text
        const xpText = document.querySelector(".xp-text");
        if (xpText) {
            const userExperience = parseInt(
                xpText.textContent.replace(" XP", "").replace(",", "")
            );

            // Calculate target width as modulo 100 (experience % 100)
            const targetWidth = (userExperience % 100) + "%";

            bar.style.width = "0%";
            setTimeout(() => {
                bar.style.width = targetWidth;
            }, 500);
        }
    });
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

// Avatar upload functionality
function initAvatarUpload() {
    const avatarInput = document.getElementById("avatar-input");
    const avatarPreview = document.getElementById("avatar-preview");

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener("change", function (e) {
            const file = e.target.files[0];

            if (file) {
                // Create preview (validation will be done on server-side)
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
    // Initialize calendar
    new ActivityCalendar();

    // Initialize animations and interactions
    animateStats();
    animateProgressBars();
    initAchievements();
    initToggleSwitches();
    initKeyboardShortcuts();
    initAvatarUpload();
});

// Export functions for potential external use
window.UserPageFunctions = {
    toggleEdit,
    showNotification,
    ActivityCalendar,
    initAvatarUpload,
};
