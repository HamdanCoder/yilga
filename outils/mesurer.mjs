#!/usr/bin/env node
// Évalue une expression JavaScript dans une page du site rendue par Chrome headless à une largeur donnée.
//   node outils/mesurer.mjs <page.html> <largeur> '<expression>' [hauteur] [--png <fichier>] [--sans-js]
// --png : capture en plus toute la page (échelle 2) dans <fichier>. --sans-js : scripts désactivés.
// Sert la racine du site sur http://127.0.0.1:8765 si rien n'y répond déjà.
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const RACINE = join(dirname(fileURLToPath(import.meta.url)), '..');
const PORT = 8765;
const args = process.argv.slice(2);
const iPng = args.indexOf('--png');
const png = iPng >= 0 ? args.splice(iPng, 2)[1] : null;
const iJs = args.indexOf('--sans-js');
const sansJs = iJs >= 0 ? (args.splice(iJs, 1), true) : false;
const [page, largeur, expression, hauteur = '900'] = args;
if (!page || !largeur || !expression) {
  console.error("usage : mesurer.mjs <page.html> <largeur> '<expression>' [hauteur]");
  process.exit(2);
}

async function serveurPret() {
  try { await fetch(`http://127.0.0.1:${PORT}/`); return true; } catch { return false; }
}

let serveur = null;
if (!(await serveurPret())) {
  serveur = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1'], { cwd: RACINE, stdio: 'ignore' });
  for (let i = 0; i < 50 && !(await serveurPret()); i++) await new Promise(r => setTimeout(r, 100));
}

const profil = mkdtempSync(join(tmpdir(), 'yilga-chrome-'));
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--remote-debugging-port=0',
  `--user-data-dir=${profil}`, `--window-size=${largeur},${hauteur}`, 'about:blank',
], { stdio: ['ignore', 'ignore', 'pipe'] });

const wsUrl = await new Promise((resolve, reject) => {
  let err = '';
  chrome.stderr.on('data', d => {
    err += d.toString();
    const m = err.match(/DevTools listening on (ws:\/\/\S+)/);
    if (m) resolve(m[1]);
  });
  chrome.on('exit', () => reject(new Error('Chrome a quitté : ' + err)));
});

const ws = new WebSocket(wsUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0;
const attentes = new Map();
const evenements = [];
ws.addEventListener('message', ev => {
  const m = JSON.parse(ev.data);
  if (m.id && attentes.has(m.id)) { attentes.get(m.id)(m); attentes.delete(m.id); }
  else if (m.method) evenements.push(m);
});
const envoyer = (method, params = {}, sessionId) => new Promise(resolve => {
  const n = ++id; attentes.set(n, resolve);
  ws.send(JSON.stringify({ id: n, method, params, sessionId }));
});
const attendre = method => new Promise(resolve => {
  const t = setInterval(() => { const i = evenements.findIndex(e => e.method === method); if (i >= 0) { clearInterval(t); resolve(evenements.splice(i, 1)[0]); } }, 20);
});

const { result: { targetId } } = await envoyer('Target.createTarget', { url: 'about:blank' });
const { result: { sessionId } } = await envoyer('Target.attachToTarget', { targetId, flatten: true });
await envoyer('Page.enable', {}, sessionId);
if (sansJs) await envoyer('Emulation.setScriptExecutionDisabled', { value: true }, sessionId);
await envoyer('Emulation.setDeviceMetricsOverride', { width: +largeur, height: +hauteur, deviceScaleFactor: 1, mobile: +largeur < 760 }, sessionId);
await envoyer('Page.navigate', { url: `http://127.0.0.1:${PORT}/${page}` }, sessionId);
await attendre('Page.loadEventFired');
// Sans script : la page est rendue sans JS ; on réactive l'exécution après le chargement, uniquement pour mesurer.
if (sansJs) await envoyer('Emulation.setScriptExecutionDisabled', { value: false }, sessionId);
await envoyer('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true }, sessionId);
const rep = await envoyer('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true }, sessionId);
if (rep.result.exceptionDetails) console.error(rep.result.exceptionDetails.text, rep.result.exceptionDetails.exception?.description ?? '');
else console.log(typeof rep.result.result.value === 'object' ? JSON.stringify(rep.result.result.value) : String(rep.result.result.value));
if (png) {
  const h = (await envoyer('Runtime.evaluate', { expression: 'document.documentElement.scrollHeight', returnByValue: true }, sessionId)).result.result.value;
  await envoyer('Emulation.setDeviceMetricsOverride', { width: +largeur, height: h, deviceScaleFactor: 2, mobile: +largeur < 760 }, sessionId);
  if (!sansJs) await envoyer('Runtime.evaluate', { expression: 'document.querySelectorAll(".reveal").forEach(s => s.classList.add("reveal--vu")); new Promise(r => setTimeout(r, 400))', awaitPromise: true }, sessionId);
  const cap = await envoyer('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true }, sessionId);
  writeFileSync(png, Buffer.from(cap.result.data, 'base64'));
  console.error(`${png} (${largeur}×${h})`);
}

ws.close();
await new Promise(r => { chrome.once('exit', r); chrome.kill(); });
if (serveur) serveur.kill();
rmSync(profil, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
