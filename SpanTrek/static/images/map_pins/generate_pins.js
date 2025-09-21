const fs = require("fs");
const path = require("path");

const pinsDir = __dirname;

// Create directory if it doesn't exist
if (!fs.existsSync(pinsDir)) {
    fs.mkdirSync(pinsDir, { recursive: true });
}

for (let i = 1; i <= 50; i++) {
    const fontSize = i < 10 ? 24 : 22; // Slightly smaller font for double digits
    const yPosition = 28; // Adjusted y position for vertical centering

    const svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
    <circle cx="20" cy="20" r="18" fill="#0a6c0dff" stroke="#FFFFFF" stroke-width="2"/>
    <text x="20" y="${yPosition}" font-family="Arial" font-size="${fontSize}" font-weight="bold" fill="#FFFFFF" text-anchor="middle">${i}</text>
</svg>`;

    const filePath = path.join(pinsDir, `pin${i}_done.svg`);
    fs.writeFileSync(filePath, svgContent);
}
