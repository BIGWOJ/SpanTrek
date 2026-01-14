// import latinize from "latinize";

// function normalizeSpanishText(text) {
//     return latinize(text)
//         .replace(/[¿¡]/g, "")
//         .replace(/,/g, "")
//         .replace(/[.!?]+$/, "")
//         .trim();
// }

// Normalize Spanish text for better comparison
function normalizeSpanishText(text) {
    // Manually normalize Spanish characters instead of using latinize
    const replacements = {
        á: "a",
        é: "e",
        í: "i",
        ó: "o",
        ú: "u",
        Á: "A",
        É: "E",
        Í: "I",
        Ó: "O",
        Ú: "U",
        ñ: "n",
        Ñ: "N",
        ü: "u",
        Ü: "U",
    };

    let normalized = text;
    for (const [spanish, english] of Object.entries(replacements)) {
        normalized = normalized.replace(new RegExp(spanish, "g"), english);
    }

    return normalized
        .replace(/[¿¡]/g, "")
        .replace(/,/g, "")
        .replace(/[.!?]+$/, "")
        .trim();
}
