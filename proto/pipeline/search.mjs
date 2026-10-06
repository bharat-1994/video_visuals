#!/usr/bin/env node
// Step 3: beats.json -> candidates.json + contact sheet (HTML). Nothing is saved except tiny previews.
// usage: node pipeline/search.mjs projects/<name> [--sources met,commons] [--limit 6]
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {searchAll} from './lib/sources.mjs';
import {download} from './lib/http.mjs';

const dir = path.resolve(process.argv[2]);
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const limit = Number(arg('limit', 5));
const only = arg('sources', '')?.split(',').filter(Boolean);
const beats = JSON.parse(fs.readFileSync(path.join(dir, 'beats.json'), 'utf8'));
const prevDir = path.join(dir, 'candidates', 'previews');
fs.mkdirSync(prevDir, {recursive: true});

const out = {};
for (const b of beats.beats) {
  const kinds = b.visual.split('+').filter((k) => k === 'image' || k === 'video');
  const seen = new Set();
  out[b.id] = [];
  for (const kind of kinds) for (const q of b.queries) {
    console.log(`[${b.id}] ${kind}: ${q}`);
    for (const c of await searchAll(q, {kind, sources: only?.length ? only : undefined, limit})) {
      if (seen.has(c.id)) continue;
      seen.add(c.id);
      if ((b.exclude || []).some((x) => c.id.includes(x) || c.title.toLowerCase().includes(x.toLowerCase()))) continue;
      out[b.id].push(c);
    }
  }
}

// small previews only (never the full asset)
for (const list of Object.values(out)) for (const c of list) {
  const f = c.id.replace(/[^a-z0-9]+/gi, '_') + '.jpg';
  c.preview = 'previews/' + f;
  const dest = path.join(prevDir, f);
  if (!fs.existsSync(dest)) {
    try {
      const raw = dest + '.raw';
      await download(c.previewUrl, raw);
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', raw, '-vf', 'scale=480:-2', '-q:v', '5', '-frames:v', '1', dest]);
      fs.rmSync(raw);
    } catch (e) { c.preview = null; }
  }
}
fs.writeFileSync(path.join(dir, 'candidates', 'candidates.json'), JSON.stringify(out, null, 2));

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (m) => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[m]));
const inline = (rel) => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(dir, 'candidates', rel)).toString('base64');
let html = `<!doctype html><meta charset=utf-8><title>Contact sheet — ${esc(beats.title)}</title>
<style>body{font:14px system-ui;background:#111;color:#ddd;margin:24px}h1{font-weight:600}h2{margin-top:36px;border-bottom:1px solid #444;padding-bottom:6px}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}.c{background:#1c1c1c;border-radius:8px;overflow:hidden}
.c img{width:100%;height:190px;object-fit:cover;display:block;background:#000}.m{padding:10px;font-size:12px;line-height:1.4}
.id{color:#f5c26b;font-weight:700}.k{color:#8ab4f8}.w{color:#ff9d8a}a{color:#8ab4f8}</style>
<h1>${esc(beats.title)}</h1><p>Approve by id (e.g. <code>b3: met:446266</code>).</p>`;
for (const b of beats.beats) {
  html += `<h2>${b.id} — ${esc(b.text)}</h2><div class=g>`;
  for (const c of out[b.id]) html += `<div class=c>${c.preview ? `<img src="${inline(c.preview)}">` : '<div style="height:190px"></div>'}<div class=m>
  <div><span class=id>${esc(c.id)}</span> <span class=k>${c.kind}${c.duration ? ' · ' + c.duration + 's' : ''}${c.width ? ' · ' + c.width + '×' + c.height : ''}</span></div>
  <div><b>${esc(c.title).slice(0, 110)}</b></div><div>${esc(c.creator).slice(0, 80)} ${esc(c.date)}</div>
  <div>Source: <a href="${esc(c.pageUrl)}">${esc(c.source)}</a></div>
  <div>License: ${esc(c.license)}${c.requiresAttribution ? ' <span class=w>(attribution required)</span>' : ''}${c.needsRightsCheck ? ' <span class=w>(verify rights)</span>' : ''}</div>
  <div style="color:#999">Credit: ${esc(c.credit).slice(0, 220)}</div></div></div>`;
  html += '</div>';
}
fs.writeFileSync(path.join(dir, 'candidates', 'contact_sheet.html'), html);
console.log('wrote', path.join(dir, 'candidates', 'contact_sheet.html'));
