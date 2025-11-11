document.addEventListener("DOMContentLoaded", function () {
    const textContent = document.querySelector(".text-content");

    if (textContent) {
        // Replace all \n with <br> tags for line breaks
        const originalText = textContent.textContent;
        const formattedText = originalText.replace(/\n/g, "<br>");
        textContent.innerHTML = formattedText;
    }
});
