// Toggle password visibility
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
