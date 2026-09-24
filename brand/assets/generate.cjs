/* Regenerate brand assets from the v4 "Academic" identity.
   Run:  NODE_PATH=$(npm root -g) node brand/assets/generate.cjs
   Bakes Newsreader / JetBrains Mono into flat PNGs (font-independent).
   Monochrome: ink on white, no accent colour. The desk tone frames the OG
   cards the way the site frames each page's sheet. Fonts are self-hosted
   (site-wide). This generator loads them straight from disk via file://
   URLs so it never depends on network access to Google Fonts through the
   proxy. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const INK = '#141414', INK2 = '#333333', GRAPHITE = '#555555';
const PAPER = '#FFFFFF', DESK = '#ECEAE4';
const SERIF = "Newsreader,Georgia,serif";
const MONO = "'JetBrains Mono',monospace";

const FONT_DIR = path.join(__dirname, '..', '..', 'assets', 'fonts');
const fontUrl = (name) => pathToFileURL(path.join(FONT_DIR, name)).href;
const FONTS = `<style>
  @font-face{font-family:"Newsreader";font-style:normal;font-weight:200 800;
    src:url("${fontUrl('newsreader-roman-latin-var.woff2')}") format("woff2");}
  @font-face{font-family:"Newsreader";font-style:italic;font-weight:200 800;
    src:url("${fontUrl('newsreader-italic-latin-var.woff2')}") format("woff2");}
  @font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:400 800;
    src:url("${fontUrl('jetbrains-mono-latin-var.woff2')}") format("woff2");}
</style>`;

function doc(inner, bg) {
  return `<!doctype html><meta charset="utf-8">${FONTS}
    <style>*{box-sizing:border-box}html,body{margin:0;padding:0;background:${bg || 'transparent'}}
    #a{display:inline-block}</style><div id="a">${inner}</div>`;
}

// Plain ink-on-white monogram, radius 0, hairline ink border. No colour, no
// logo mark; the letterform in Newsreader is the identity.
function icon(size, letter, fs_) {
  const border = size >= 180 ? 1.5 : 0.5;
  return `<div style="width:${size}px;height:${size}px;background:${PAPER};
    border:${border}px solid ${INK};box-sizing:border-box;
    display:flex;align-items:center;justify-content:center;overflow:hidden">
    <span style="font-family:${SERIF};font-weight:500;color:${INK};font-size:${fs_}px;
      letter-spacing:-.01em;line-height:1">${letter}</span></div>`;
}

// Stacked "Angelo / Boutalikakis" wordmark, ink on white or paper on ink.
function wordmark(reversed) {
  const bg = reversed ? INK : PAPER, fg = reversed ? PAPER : INK;
  return `<div style="background:${bg};padding:96px 110px;display:inline-block;font-family:${SERIF};
    font-weight:500;letter-spacing:-.01em;line-height:1.05;font-size:150px;color:${fg}">
    <div>Angelo</div><div>Boutalikakis</div></div>`;
}

// Generic 1200x630 share card: a white sheet, framed by the desk tone, the
// way every page frames its sheet. `kicker` is the mono top-left label
// (rendered uppercase via text-transform). `mainText` is either the plain
// name ("Angelo Boutalikakis", set in Newsreader, one word per line) or,
// for work cards, a project slug (set in JetBrains Mono, `mono: true`).
// `serifLine` is the italic Newsreader line underneath; long lines shrink
// and wrap so they never overflow the fixed-height card.
function ogCard(kicker, mainText, serifLine, opts) {
  opts = opts || {};
  const long = serifLine.length > 38;
  const serifSize = long ? 28 : 40;
  const serifStyle = long
    ? `font-size:${serifSize}px;line-height:1.3;max-width:760px`
    : `font-size:${serifSize}px;line-height:1.25`;
  const mainBlock = opts.mono
    ? `<div style="font-family:${MONO};font-weight:500;font-size:56px;letter-spacing:-.01em;color:${INK}">${mainText}</div>`
    : `<div style="font-family:${SERIF};font-weight:500;line-height:1.05;font-size:92px;color:${INK}">${mainText.split(' ').map((w) => `<div>${w}</div>`).join('')}</div>`;
  return `<div style="width:1200px;height:630px;background:${DESK};padding:34px;box-sizing:border-box;font-family:${SERIF}">
    <div style="width:100%;height:100%;background:${PAPER};border:.5px solid ${INK};box-sizing:border-box;
      padding:72px;display:flex;flex-direction:column;justify-content:space-between">
      <div style="font-family:${MONO};font-size:18px;letter-spacing:.14em;text-transform:uppercase;color:${GRAPHITE}">${kicker}</div>
      <div>${mainBlock}
        <div style="margin-top:28px;font-style:italic;color:${INK2};${serifStyle}">${serifLine}</div>
      </div>
    </div>
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
  { f: 'favicon-16.png',        html: doc(icon(16, 'A', 10)) },
  { f: 'favicon-32.png',        html: doc(icon(32, 'A', 20)) },
  { f: 'favicon-48.png',        html: doc(icon(48, 'A', 30)) },
  { f: 'apple-touch-icon.png',  html: doc(icon(180, 'A', 108)) },
  { f: 'icon-512.png',          html: doc(icon(512, 'A', 308)) },
  { f: 'avatar-512.png',        html: doc(icon(512, 'AB', 190)) },
  { f: 'wordmark-light.png',    html: doc(wordmark(false)) },
  { f: 'wordmark-reversed.png', html: doc(wordmark(true)) },
  { f: 'og-image.png',          html: doc(ogCard('Angelo Boutalikakis &middot; Selected work', 'Angelo Boutalikakis', 'Operator, product builder, and transformation leader'), DESK) },
  { f: 'og-about.png',          html: doc(ogCard('Angelo Boutalikakis &middot; About', 'Angelo Boutalikakis', 'Operator, product builder, and transformation leader.'), DESK) },
  { f: 'og-writing.png',        html: doc(ogCard('Angelo Boutalikakis &middot; Writing', 'Angelo Boutalikakis', 'Research, publications, and talks.'), DESK) },
  { f: 'og-cv.png',             html: doc(ogCard('Angelo Boutalikakis &middot; Curriculum Vitae', 'Angelo Boutalikakis', 'Engagement Manager, McKinsey &amp; Company.'), DESK) },
  { f: 'og-post-hello-world.png', html: doc(ogCard('Angelo Boutalikakis &middot; Writing', 'Angelo Boutalikakis', 'Hello, world &middot; what this site is'), DESK) },
  ...WORK_CARDS.map((w) => ({
    f: `og-work-${w.slug}.png`,
    html: doc(ogCard('Angelo Boutalikakis &middot; Work', w.slug, w.line, { mono: true }), DESK),
  })),
];

async function waitForFonts(p) {
  await p.evaluate(() => document.fonts.ready);
  for (let i = 0; i < 50; i++) {
    const ok = await p.evaluate(() =>
      document.fonts.check('500 40px Newsreader') &&
      document.fonts.check('italic 400 40px Newsreader') &&
      document.fonts.check('500 40px "JetBrains Mono"'));
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
    const ok = await waitForFonts(p);
    await p.waitForTimeout(300); // let Newsreader/JetBrains settle too
    const el = await p.$('#a');
    await el.screenshot({ path: path.join(__dirname, j.f), omitBackground: true });
    console.log((ok ? 'OK  ' : 'WARN(fallback) ') + j.f);
  }
  fs.unlinkSync(tmp);
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
