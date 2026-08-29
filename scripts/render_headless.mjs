// Headless Diffusion Studio renderer driver.
// Bundles scripts/render-entry.mjs (which uses @diffusionstudio/core) with
// esbuild, loads it in headless Chromium (Playwright), and writes the
// resulting video Blob to disk. Core needs a real browser (Canvas2D/WebCodecs),
// so this cannot run under plain Node.
import { chromium } from 'playwright';
import * as esbuild from 'esbuild';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

const args = process.argv.slice(2);
let out = 'rendered.webm';
let specPath = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out') out = args[++i];
  else if (args[i] === '--spec') specPath = args[++i];
}

const spec =
  specPath && existsSync(specPath)
    ? JSON.parse(readFileSync(specPath, 'utf8'))
    : {
        width: 1920,
        height: 1080,
        background: '#0b0e14',
        clips: [
          { type: 'text', text: 'Delta Force — Coaching', fontSize: 96, start: 0, end: 3 },
          { type: 'rect', fill: '#e8482b', x: 720, y: 430, width: 480, height: 220, start: 0, end: 3 },
          { type: 'text', text: 'Hold the container mouth, then take the lane.', fontSize: 60, y: 560, start: 1, end: 3 },
        ],
      };

const bundle = (
  await esbuild.build({
    entryPoints: [resolve(__dirname, 'render-entry.mjs')],
    bundle: true,
    format: 'iife',
    platform: 'browser',
    write: false,
    logLevel: 'silent',
  })
).outputFiles[0].text;

const browser = await chromium.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
});
const page = await browser.newPage();
await page.setViewportSize({ width: spec.width || 1920, height: spec.height || 1080 });
await page.goto('about:blank');
await page.addScriptTag({ content: bundle });

const res = await page.evaluate((s) => window.__render(s), spec);
await browser.close();

const ext = (res.type || '').includes('mp4') ? 'mp4' : 'webm';
const file = out.replace(/\.(webm|mp4)$/i, '') + '.' + ext;
writeFileSync(file, Buffer.from(res.b64, 'base64'));
console.log(`WROTE ${file} (${(Buffer.from(res.b64, 'base64').length)} bytes, type=${res.type})`);
