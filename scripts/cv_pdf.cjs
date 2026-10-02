#!/usr/bin/env node
// Print /cv/ to PDF with Playwright Chromium.
//
// Usage:
//   NODE_PATH=$(npm root -g) node scripts/cv_pdf.cjs <base-url> [out.pdf]
//
// <base-url> is a running static server for the repo root, for example
// http://localhost:8842 (python3 -m http.server 8842). The script serves
// nothing itself. out.pdf defaults to cv/Angelo-Boutalikakis-CV.pdf in the
// repo. .github/workflows/cv-pdf.yml runs this on every CV, stylesheet, font
// or headshot change.
//
// Settings: print media, fonts loaded, A4, no background graphics, 15 mm
// margins on every side.

const path = require('path');
const { chromium } = require('playwright');

const base = process.argv[2];
if (!base) {
  console.error('usage: node scripts/cv_pdf.cjs <base-url> [out.pdf]');
  process.exit(2);
}
const out = path.resolve(
  process.argv[3] || path.join(__dirname, '..', 'cv', 'Angelo-Boutalikakis-CV.pdf')
);
const url = base.replace(/\/+$/, '') + '/cv/';

(async () => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    const res = await page.goto(url);
    if (!res || !res.ok()) {
      throw new Error('GET ' + url + ' returned ' + (res ? res.status() : 'no response'));
    }
    await page.emulateMedia({ media: 'print' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: out,
      format: 'A4',
      printBackground: false,
      margin: { top: '15mm', right: '15mm', bottom: '15mm', left: '15mm' },
    });
    console.log('Wrote ' + out);
  } finally {
    await browser.close();
  }
})().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
