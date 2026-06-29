/* Regenerate brand assets from the locked anchors.
   Run:  NODE_PATH=$(npm root -g) node brand/assets/generate.cjs
   Bakes Archivo / Newsreader / JetBrains Mono into flat PNGs (font-independent). */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const INK = '#17171A', PAPER = '#FAF8F4', STONE = '#9B9890';
const BLUE = '#2C46C8', BLUED = '#1B2E8F';
const SANS = "Archivo,'Helvetica Neue',Helvetica,Arial,sans-serif";
const FONTS =
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' +
  '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;800&family=Newsreader:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">';

function doc(inner) {
  return `<!doctype html><meta charset="utf-8">${FONTS}
    <style>*{box-sizing:border-box}html,body{margin:0;padding:0;background:transparent}
    #a{display:inline-block}</style><div id="a">${inner}</div>`;
}
function icon(size, radius, letter, fs_) {
  return `<div style="width:${size}px;height:${size}px;border-radius:${radius}px;background:${BLUE};
    display:flex;align-items:center;justify-content:center;overflow:hidden">
    <span style="font-family:${SANS};font-weight:800;color:${PAPER};font-size:${fs_}px;
      letter-spacing:-.04em;line-height:1;transform:translateY(-3%)">${letter}</span></div>`;
}
function wordmark(onBlue) {
  const bg = onBlue ? BLUE : PAPER, first = onBlue ? PAPER : INK, sur = onBlue ? PAPER : BLUE;
  return `<div style="background:${bg};padding:96px 110px;display:inline-block;font-family:${SANS};
    font-weight:700;letter-spacing:-.035em;line-height:.88;font-size:170px">
    <div style="color:${first}">Angelo</div><div style="color:${sur}">Boutalikakis</div></div>`;
}
function og() {
  return `<div style="width:1200px;height:630px;background:${PAPER};padding:90px;display:flex;
    flex-direction:column;justify-content:space-between;font-family:${SANS}">
    <div style="font-family:'JetBrains Mono',monospace;font-size:20px;letter-spacing:.16em;text-transform:uppercase;color:${STONE}">Angelo Boutalikakis &mdash; Selected work</div>
    <div style="font-weight:700;letter-spacing:-.035em;line-height:.86;font-size:132px">
      <span style="color:${INK}">Angelo</span><br><span style="color:${BLUE}">Boutalikakis</span></div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end">
      <div style="font-family:Newsreader,Georgia,serif;font-style:italic;font-size:44px;color:${BLUED}">Curiosity meets rigor.</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:18px;color:${STONE}">ZURICH / BRUSSELS &middot; 2026</div></div>
  </div>`;
}

const JOBS = [
  { f: 'favicon-16.png',        html: doc(icon(16, 2, 'A', 11)) },
  { f: 'favicon-32.png',        html: doc(icon(32, 4, 'A', 22)) },
  { f: 'favicon-48.png',        html: doc(icon(48, 6, 'A', 33)) },
  { f: 'apple-touch-icon.png',  html: doc(icon(180, 40, 'A', 120)) },
  { f: 'icon-512.png',          html: doc(icon(512, 114, 'A', 340)) },
  { f: 'avatar-512.png',        html: doc(icon(512, 114, 'AB', 210)) },
  { f: 'wordmark-light.png',    html: doc(wordmark(false)) },
  { f: 'wordmark-reversed.png', html: doc(wordmark(true)) },
  { f: 'og-image.png',          html: doc(og()) },
];

async function waitForArchivo(p) {
  await p.evaluate(() => document.fonts.ready);
  for (let i = 0; i < 50; i++) {
    const ok = await p.evaluate(() =>
      document.fonts.check('800 40px Archivo') && document.fonts.check('700 40px Archivo'));
    if (ok) return true;
    await p.waitForTimeout(200);
  }
  return false;
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 2 });
  const tmp = path.join(__dirname, '_tmp.html');
  for (const j of JOBS) {
    fs.writeFileSync(tmp, j.html);
    await p.goto('file://' + tmp, { waitUntil: 'load' });
    const ok = await waitForArchivo(p);
    await p.waitForTimeout(300); // let Newsreader/JetBrains settle too
    const el = await p.$('#a');
    await el.screenshot({ path: path.join(__dirname, j.f), omitBackground: true });
    console.log((ok ? 'OK  ' : 'WARN(fallback) ') + j.f);
  }
  fs.unlinkSync(tmp);
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
