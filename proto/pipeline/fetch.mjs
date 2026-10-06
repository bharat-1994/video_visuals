#!/usr/bin/env node
// Step 5: approvals.json -> saves ONLY the approved clips + writes the license/credit ledger.
// usage: node pipeline/fetch.mjs projects/<name>
//
// approvals.json: { "<beatId>": [ {id, as, start?, duration?, crop?, note?} ] }
//  - images are downloaded as-is
//  - videos are cut server-side with ffmpeg range requests (start/duration), so a 27-min source never lands on disk
// Output: proto/public/<name>/<as>, projects/<name>/credits.json, projects/<name>/CREDITS.md
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {download, UA} from './lib/http.mjs';

const dir = path.resolve(process.argv[2]);
const name = path.basename(dir);
const pub = path.resolve(dir, '../../public', name);
fs.mkdirSync(pub, {recursive: true});

const approvals = JSON.parse(fs.readFileSync(path.join(dir, 'approvals.json'), 'utf8'));
const cands = Object.values(JSON.parse(fs.readFileSync(path.join(dir, 'candidates', 'candidates.json'), 'utf8'))).flat();
const byId = new Map(cands.map((c) => [c.id, c]));
const ledger = [];

for (const [beat, picks] of Object.entries(approvals)) for (const p of picks) {
  const c = byId.get(p.id);
  if (!c) throw new Error(`${p.id} is not in candidates.json — re-run search`);
  if (c.needsRightsCheck && !p.rightsVerified) throw new Error(`${p.id}: LoC-style item needs "rightsVerified": true after you check ${c.pageUrl}`);
  if (c.needsFileResolve) throw new Error(`${p.id}: archive.org item needs a concrete file — add "url" to the approval`);
  const dest = path.join(pub, p.as);
  if (!fs.existsSync(dest)) {
    const src = p.url || c.downloadUrl;
    if (c.kind === 'video') {
      const vf = [p.crop ? `crop=${p.crop}` : null, 'fps=30'].filter(Boolean).join(',');
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-user_agent', UA, ...(p.start ? ['-ss', String(p.start)] : []), '-t', String(p.duration || 8), '-i', src,
        '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', dest], {stdio: 'inherit'});
    } else {
      await download(src, dest);
    }
    console.log('saved', path.relative(process.cwd(), dest));
  }
  ledger.push({
    beat, file: `public/${name}/${p.as}`, id: c.id, kind: c.kind, title: c.title, creator: c.creator, date: c.date,
    source: c.source, pageUrl: c.pageUrl, license: c.license, licenseUrl: c.licenseUrl,
    requiresAttribution: c.requiresAttribution, credit: c.credit, usage: p.note || '', segment: p.start != null ? {start: p.start, duration: p.duration || 8} : undefined,
  });
}
fs.writeFileSync(path.join(dir, 'credits.json'), JSON.stringify(ledger, null, 2));

let md = `# Credits — ${name}\n\nEvery asset in this video, with source and license. Items marked **attribution required** must be credited in the video description.\n\n`;
for (const l of ledger) md += `- **${l.title}** — ${l.creator}${l.date ? ', ' + l.date : ''}  \n  Source: ${l.source} <${l.pageUrl}>  \n  License: ${l.license}${l.requiresAttribution ? ' **(attribution required)**' : ''}  \n  Used in beat ${l.beat} as \`${l.file}\`${l.usage ? ' — ' + l.usage : ''}\n`;
fs.writeFileSync(path.join(dir, 'CREDITS.md'), md);
console.log(`ledger: ${ledger.length} assets -> ${path.join(dir, 'CREDITS.md')}`);
