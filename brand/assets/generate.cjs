/* Regenerate brand assets from the locked anchors.
   Run:  NODE_PATH=$(npm root -g) node brand/assets/generate.cjs
   Bakes Archivo / Newsreader / JetBrains Mono into flat PNGs (font-independent).
   Fonts are self-hosted (site-wide as of the font self-host migration) — this
   generator loads them straight from disk via file:// URLs so it never
   depends on network access to Google Fonts through the proxy. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const INK = '#17171A', PAPER = '#FAF8F4', STONE = '#9B9890';
const BLUE = '#2C46C8', BLUED = '#1B2E8F';
const SANS = "Archivo,'Helvetica Neue',Helvetica,Arial,sans-serif";

const FONT_DIR = path.join(__dirname, '..', '..', 'assets', 'fonts');
const fontUrl = (name) => pathToFileURL(path.join(FONT_DIR, name)).href;
const FONTS = `<style>
  @font-face{font-family:"Archivo";font-style:normal;font-weight:100 900;
    src:url("${fontUrl('archivo-latin-var.woff2')}") format("woff2");}
  @font-face{font-family:"Newsreader";font-style:normal;font-weight:400;
    src:url("${fontUrl('newsreader-regular-latin-var.woff2')}") format("woff2");}
  @font-face{font-family:"Newsreader";font-style:italic;font-weight:200 800;
    src:url("${fontUrl('newsreader-italic-latin-var.woff2')}") format("woff2");}
  @font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:400 800;
    src:url("${fontUrl('jetbrains-mono-latin-var.woff2')}") format("woff2");}
</style>`;

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
// Generic 1200x630 share card. `kicker` is the mono top-left label (rendered
// uppercase via text-transform, so pass normal casing). `serifLine` is the bottom-left
// Newsreader-italic context line — long project one-liners auto-shrink and
// wrap so they never overflow the fixed-height card.
function ogCard(kicker, serifLine) {
  const long = serifLine.length > 38;
  const serifSize = long ? 30 : 44;
  const serifStyle = long
    ? `font-size:${serifSize}px;line-height:1.25;max-width:720px`
    : `font-size:${serifSize}px;line-height:1.2`;
  return `<div style="width:1200px;height:630px;background:${PAPER};padding:90px;display:flex;
    flex-direction:column;justify-content:space-between;font-family:${SANS}">
    <div style="font-family:'JetBrains Mono',monospace;font-size:20px;letter-spacing:.16em;text-transform:uppercase;color:${STONE}">${kicker}</div>
    <div style="font-weight:700;letter-spacing:-.035em;line-height:.86;font-size:132px">
      <span style="color:${INK}">Angelo</span><br><span style="color:${BLUE}">Boutalikakis</span></div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end">
      <div style="font-family:Newsreader,Georgia,serif;font-style:italic;color:${BLUED};${serifStyle}">${serifLine}</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:18px;color:${STONE};white-space:nowrap;flex-shrink:0;margin-left:24px">ZURICH / BRUSSELS &middot; 2026</div></div>
  </div>`;
}

const WORK_CARDS = [
  { slug: 'gesundheit-mcp',
    line: 'MCP server on Swiss health-insurance and healthcare data.' },
  { slug: 'life-improver',
    line: 'Interactive framework of meaningful life practices from psychology, philosophy, and contemplative traditions.' },
  { slug: 'edition-guru',
    line: 'Scrapes art print galleries, enriches new drops with market data and LLM descriptions, emails a newsletter.' },
  { slug: 'bxl_eda_worker',
    line: 'Daily digest of EU foreign-policy, Middle East, and sanctions news for a Swiss reader.' },
  { slug: 'cloudy-plag',
    line: 'Documents credibility issues in dissertations.' },
  { slug: 'cleardoc',
    line: 'Optimizes invoices for Swiss healthcare practitioners.' },
];

const JOBS = [
  { f: 'favicon-16.png',        html: doc(icon(16, 2, 'A', 11)) },
  { f: 'favicon-32.png',        html: doc(icon(32, 4, 'A', 22)) },
  { f: 'favicon-48.png',        html: doc(icon(48, 6, 'A', 33)) },
  { f: 'apple-touch-icon.png',  html: doc(icon(180, 40, 'A', 120)) },
  { f: 'icon-512.png',          html: doc(icon(512, 114, 'A', 340)) },
  { f: 'avatar-512.png',        html: doc(icon(512, 114, 'AB', 210)) },
  { f: 'wordmark-light.png',    html: doc(wordmark(false)) },
  { f: 'wordmark-reversed.png', html: doc(wordmark(true)) },
  { f: 'og-image.png',          html: doc(ogCard('Angelo Boutalikakis &middot; Selected work', 'I build and ship tools with AI, from scheduled workers to an MCP server on Swiss health data.')) },
  { f: 'og-about.png',          html: doc(ogCard('Angelo Boutalikakis &middot; About', 'Operator, product builder, and transformation leader.')) },
  { f: 'og-writing.png',        html: doc(ogCard('Angelo Boutalikakis &middot; Writing', 'Research, publications, and talks.')) },
  { f: 'og-cv.png',             html: doc(ogCard('Angelo Boutalikakis &middot; Curriculum Vitae', 'Engagement Manager, McKinsey &amp; Company.')) },
  { f: 'og-post-hello-world.png', html: doc(ogCard('Angelo Boutalikakis &middot; Writing', 'Hello, world &middot; what this site is')) },
  ...WORK_CARDS.map(w => ({
    f: `og-work-${w.slug}.png`,
    html: doc(ogCard('Angelo Boutalikakis &middot; Work', w.line)),
  })),
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
