// Renders a reel HTML (it must define seek(t) and DURATION) to JPG frames.
// Run from the reel folder:  HTML=reel_ar.html OUT=frames node <plugin>/templates/explainer/render.js all
//                            HTML=reel_ar.html OUT=prev  node <plugin>/templates/explainer/render.js preview 3 8.5
// Needs puppeteer-core (npm i puppeteer-core) and Chrome. Env: PUPPETEER_PATH, CHROME_PATH.
const path = require('path'), fs = require('fs');
const puppeteer = require(process.env.PUPPETEER_PATH || 'puppeteer-core');
const DIR = process.cwd(), FPS = 30, HTML = process.env.HTML || 'anim.html', OUT = process.env.OUT || 'frames';
const CHROME = process.env.CHROME_PATH || ({
  darwin: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  win32: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  linux: '/usr/bin/google-chrome'
})[process.platform];
(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new' });
  const p = await b.newPage();
  await p.setViewport({ width: 720, height: 1280, deviceScaleFactor: 1.5 });   // 1080x1920 output
  await p.goto('file://' + path.join(DIR, HTML), { waitUntil: 'networkidle0' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => window.READY || true);
  const mode = process.argv[2] || 'all';
  if (mode === 'preview') {
    fs.mkdirSync(path.join(DIR, 'prev'), { recursive: true });
    for (const t of process.argv.slice(3).map(Number)) {
      await p.evaluate(t => seek(t), t);
      await p.screenshot({ path: path.join(DIR, 'prev', `${OUT}_${String(t.toFixed(2)).padStart(5, '0')}.png`) });
    }
  } else {
    const out = path.join(DIR, OUT); fs.mkdirSync(out, { recursive: true });
    const D = await p.evaluate(() => DURATION), N = Math.round(D * FPS);
    for (let i = 0; i < N; i++) {
      await p.evaluate(t => seek(t), i / FPS);
      await p.screenshot({ path: path.join(out, String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
      if (i % 60 === 0) console.log(`${i}/${N}`);
    }
  }
  await b.close();
})();
