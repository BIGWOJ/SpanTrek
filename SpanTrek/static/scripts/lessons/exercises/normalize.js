import latinize from "latinize";

// Normalize Spanish text for better comparison
function normalizeSpanishText(text) {
    return latinize(text)
        .replace(/[¿¡]/g, "")
        .replace(/,/g, "")
        .replace(/[.!?]+$/, "")
        .trim();
}
