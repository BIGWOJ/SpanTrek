// Toggle password visibility function
function togglePasswordVisibility(index) {
    const pwdInput = document.getElementById(`password-input-${index}`);
    const icon = document.getElementById(`toggle-password-icon-${index}`);
    if (pwdInput.type === "password") {
        pwdInput.type = "text";
        icon.textContent = "🔓";
    } else {
        pwdInput.type = "password";
        icon.textContent = "🔒";
    }
}

// Move password input to wrapper on page load
document.addEventListener("DOMContentLoaded", function () {
    // Clear form fields on page load/refresh
    clearFormFields();

    // Find all password inputs but exclude password confirmation fields
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    let toggleIndex = 0; // Separate counter for toggle buttons

    passwordInputs.forEach((pwdInput) => {
        // Skip password confirmation fields (common names for confirmation fields)
        const fieldName = pwdInput.name.toLowerCase();
        const fieldPlaceholder = pwdInput.placeholder
            ? pwdInput.placeholder.toLowerCase()
            : "";

        // Check both name and placeholder for confirmation field indicators
        if (
            fieldName.includes("confirm") ||
            fieldName.includes("confirmation") ||
            fieldName.includes("repeat") ||
            fieldName.includes("verify") ||
            fieldName.includes("password2") ||
            fieldName.includes("password_confirm") ||
            fieldPlaceholder.includes("confirm") ||
            fieldPlaceholder.includes("repeat")
        ) {
            return; // Skip this field, don't add toggle button
        }

        // Give each main password input a unique ID
        pwdInput.id = `password-input-${toggleIndex}`;

        const wrapper = document.createElement("div");
        wrapper.className = "password-wrapper";
        pwdInput.parentNode.insertBefore(wrapper, pwdInput);
        wrapper.appendChild(pwdInput);

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "toggle-password";
        btn.id = `toggle-password-icon-${toggleIndex}`;
        btn.textContent = "🔒";

        // Create a closure to capture the current toggleIndex value
        btn.onclick = (function (currentIndex) {
            return function () {
                togglePasswordVisibility(currentIndex);
            };
        })(toggleIndex);

        wrapper.appendChild(btn);

        toggleIndex++; // Increment only for fields that get toggle buttons
    });

    // Add password confirmation validation
    setupPasswordConfirmationValidation();
});

// Function to clear all form fields
function clearFormFields() {
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');

    if (emailInput) {
        emailInput.value = "";
    }
    if (passwordInput) {
        passwordInput.value = "";
        passwordInput.type = "password"; // Reset password field to hidden
    }

    // Clear any other form inputs if they exist
    const allInputs = document.querySelectorAll(
        'input[type="text"], input[type="email"], input[type="password"]'
    );
    allInputs.forEach((input) => {
        input.value = "";
    });
}

// Function to setup password confirmation validation
function setupPasswordConfirmationValidation() {
    const password1 = document.querySelector('input[name="password1"]');
    const password2 = document.querySelector('input[name="password2"]');

    if (password1 && password2) {
        // Function to validate passwords
        function validatePasswords() {
            if (password2.value.length > 0) {
                if (password1.value !== password2.value) {
                    password2.classList.remove("password-match");
                    password2.classList.add("password-mismatch");
                } else {
                    password2.classList.remove("password-mismatch");
                    password2.classList.add("password-match");
                }
            } else {
                // Reset to default styling when field is empty
                password2.classList.remove(
                    "password-mismatch",
                    "password-match"
                );
            }
        }

        // Add event listeners to both password fields
        password1.addEventListener("input", validatePasswords);
        password2.addEventListener("input", validatePasswords);
        password2.addEventListener("blur", validatePasswords);
    }
}
