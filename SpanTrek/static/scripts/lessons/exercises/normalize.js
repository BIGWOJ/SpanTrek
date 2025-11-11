/**
 * Normalize Spanish text by converting special characters to English equivalents
 * This allows for accent-insensitive comparison of user answers
 *
 * @param {string} text - The text to normalize
 * @returns {string} Normalized text with Spanish characters replaced
 *
 * @example
 * normalizeSpanishText("pequeña") // returns "pequena"
 * normalizeSpanishText("José") // returns "Jose"
 */
function normalizeSpanishText(text) {
    const spanishToEnglish = {
        á: "a",
        à: "a",
        ä: "a",
        â: "a",
        é: "e",
        è: "e",
        ë: "e",
        ê: "e",
        í: "i",
        ì: "i",
        ï: "i",
        î: "i",
        ó: "o",
        ò: "o",
        ö: "o",
        ô: "o",
        ú: "u",
        ù: "u",
        ü: "u",
        û: "u",
        ñ: "n",
        ç: "c",
        Á: "A",
        À: "A",
        Ä: "A",
        Â: "A",
        É: "E",
        È: "E",
        Ë: "E",
        Ê: "E",
        Í: "I",
        Ì: "I",
        Ï: "I",
        Î: "I",
        Ó: "O",
        Ò: "O",
        Ö: "O",
        Ô: "O",
        Ú: "U",
        Ù: "U",
        Ü: "U",
        Û: "U",
        Ñ: "N",
        Ç: "C",
    };

    let normalized = text;
    for (const [spanish, english] of Object.entries(spanishToEnglish)) {
        normalized = normalized.replace(new RegExp(spanish, "g"), english);
    }
    return normalized;
}
