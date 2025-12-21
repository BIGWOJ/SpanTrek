import latinize from "latinize";

function normalizeSpanishText(text) {
    return latinize(text)
        .replace(/[¿¡]/g, "")
        .replace(/,/g, "")
        .replace(/[.!?]+$/, "")
        .trim();
}
