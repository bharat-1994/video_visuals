// Cached, rate-limit-aware JSON/file fetching shared by all source adapters.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export const UA = 'video-visuals-pipeline/0.1 (chandrabharat080@gmail.com)';
const CACHE = path.resolve(import.meta.dirname, '../.cache');
fs.mkdirSync(CACHE, {recursive: true});

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const lastHit = {};

async function politely(url, opts = {}, tries = 6) {
  const host = new URL(url).host;
  // Wikimedia is strict; space requests out.
  const gap = /wikimedia|wikipedia/.test(host) ? 1500 : 150;
  for (let i = 0; i < tries; i++) {
    const wait = (lastHit[host] || 0) + gap - Date.now();
    if (wait > 0) await sleep(wait);
    lastHit[host] = Date.now();
    const res = await fetch(url, {...opts, headers: {'User-Agent': UA, ...(opts.headers || {})}});
    if (res.status === 429 || res.status >= 500) {
      const ra = Number(res.headers.get('retry-after')) || 0;
      await sleep(Math.max(ra * 1000, 2000 * 2 ** i));
      continue;
    }
    return res;
  }
  throw new Error(`gave up after ${tries} tries: ${url}`);
}

export async function getJSON(url, {cache = true, headers} = {}) {
  // Cache key must not include secrets.
  const safe = url.replace(/([?&]key=)[^&]+/, '$1_');
  const f = path.join(CACHE, crypto.createHash('sha1').update(safe).digest('hex') + '.json');
  if (cache && fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8'));
  const res = await politely(url, {headers});
  if (!res.ok) throw new Error(`${res.status} ${safe}`);
  const text = await res.text();
  let j;
  try { j = JSON.parse(text); } catch { throw new Error(`non-JSON from ${safe}: ${text.slice(0, 120)}`); }
  if (cache) fs.writeFileSync(f, text);
  return j;
}

export async function download(url, dest) {
  fs.mkdirSync(path.dirname(dest), {recursive: true});
  const res = await politely(url);
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  fs.writeFileSync(dest, Buffer.from(await res.arrayBuffer()));
  return dest;
}

export const strip = (s) => (s || '').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
