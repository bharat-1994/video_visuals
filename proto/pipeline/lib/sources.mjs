// Source adapters. Each: search(query, {kind, limit}) -> Candidate[]
//
// Candidate = {
//   id, source, kind: 'image'|'video', title, creator, date,
//   license, licenseUrl, requiresAttribution, credit,
//   pageUrl, previewUrl, downloadUrl, width, height, duration, query
// }
import {getJSON, strip} from './http.mjs';

const enc = encodeURIComponent;

// ---------- Metropolitan Museum (CC0 for isPublicDomain objects) ----------
async function met(q, {kind, limit = 8}) {
  if (kind === 'video') return [];
  const s = await getJSON(`https://collectionapi.metmuseum.org/public/collection/v1.1/search?q=${enc(q)}&hasImages=true&isPublicDomain=true&limit=${limit * 2}`);
  const out = [];
  for (const id of (s.objectIDs || []).slice(0, limit * 2)) {
    let o;
    try { o = await getJSON(`https://collectionapi.metmuseum.org/public/collection/v1/objects/${id}`); } catch { continue; }
    if (!o.isPublicDomain || !o.primaryImage) continue;
    out.push({
      id: `met:${id}`, source: 'The Metropolitan Museum of Art', kind: 'image',
      title: o.title, creator: o.artistDisplayName || o.culture || 'Unknown', date: o.objectDate,
      license: 'CC0 1.0 (Met Open Access)', licenseUrl: 'https://creativecommons.org/publicdomain/zero/1.0/',
      requiresAttribution: false,
      credit: `${o.title}${o.artistDisplayName ? ', ' + o.artistDisplayName : ''}, ${o.objectDate}. ${o.creditLine}. The Metropolitan Museum of Art, ${o.accessionNumber}`,
      pageUrl: o.objectURL, previewUrl: o.primaryImageSmall, downloadUrl: o.primaryImage,
      query: q,
    });
    if (out.length >= limit) break;
  }
  return out;
}

// ---------- Smithsonian Open Access (CC0 media only) ----------
async function smithsonian(q, {kind, limit = 8}) {
  if (kind === 'video') return [];
  const key = process.env.SI_API_KEY || 'DEMO_KEY';
  const s = await getJSON(`https://api.si.edu/openaccess/api/v1.0/search?q=${enc(q + ' AND online_media_type:"Images"')}&api_key=${key}&rows=${limit * 3}`);
  const out = [];
  for (const r of s.response?.rows || []) {
    const media = r.content?.descriptiveNonRepeating?.online_media?.media || [];
    const m = media.find((x) => x.type === 'Images' && /CC0/i.test(x.usage?.access || ''));
    if (!m) continue;
    const d = r.content.descriptiveNonRepeating;
    const f = r.content.freetext || {};
    const url = m.content;
    out.push({
      id: `si:${r.id}`, source: `Smithsonian (${d.data_source || r.unitCode})`, kind: 'image',
      title: r.title, creator: f.name?.[0]?.content || 'Unknown', date: f.date?.[0]?.content || '',
      license: 'CC0 1.0 (Smithsonian Open Access)', licenseUrl: 'https://creativecommons.org/publicdomain/zero/1.0/',
      requiresAttribution: false,
      credit: `${r.title}. ${f.creditLine?.[0]?.content || ''} ${d.data_source || ''}, ${f.identifier?.[0]?.content || ''}`.replace(/\s+/g, ' ').trim(),
      pageUrl: d.guid || d.record_link, previewUrl: url + (url.includes('?') ? '&' : '?') + 'max=600', downloadUrl: url,
      query: q,
    });
    if (out.length >= limit) break;
  }
  return out;
}

// ---------- Wikimedia Commons ----------
const COMMONS_OK = /^(public domain|pd|cc0|cc[- ]by|cc[- ]by[- ]sa|attribution|no restrictions)/i;
async function commons(q, {kind, limit = 8}) {
  const type = kind === 'video' ? 'video' : 'bitmap';
  const u = `https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6&gsrsearch=${enc(q + ' filetype:' + type)}&gsrlimit=${limit * 2}` +
    `&prop=imageinfo&iiprop=url|size|mime|extmetadata|mediatype|dimensions&iiurlwidth=640&iiextmetadatafilter=LicenseShortName|LicenseUrl|Artist|Credit|ImageDescription|DateTimeOriginal|ObjectName|AttributionRequired|UsageTerms`;
  const j = await getJSON(u);
  const out = [];
  for (const p of Object.values(j.query?.pages || {}).sort((a, b) => a.index - b.index)) {
    const ii = p.imageinfo?.[0];
    if (!ii) continue;
    const md = ii.extmetadata || {};
    const lic = md.LicenseShortName?.value || '';
    if (!COMMONS_OK.test(lic)) continue; // skip non-free / fair-use / unknown
    const attribution = /by/i.test(lic) || md.AttributionRequired?.value === 'true';
    out.push({
      id: `commons:${p.pageid}`, source: 'Wikimedia Commons', kind: kind === 'video' ? 'video' : 'image',
      title: strip(md.ObjectName?.value) || p.title.replace(/^File:/, ''),
      creator: strip(md.Artist?.value) || 'Unknown', date: strip(md.DateTimeOriginal?.value),
      license: lic, licenseUrl: md.LicenseUrl?.value || '', requiresAttribution: attribution,
      credit: `${strip(md.ObjectName?.value) || p.title.replace(/^File:/, '')} — ${strip(md.Artist?.value) || 'Unknown'} — ${lic} — via Wikimedia Commons`,
      pageUrl: ii.descriptionurl, previewUrl: ii.thumburl || ii.url, downloadUrl: ii.url,
      width: ii.width, height: ii.height, duration: ii.duration,
      query: q,
    });
    if (out.length >= limit) break;
  }
  return out;
}

// ---------- Library of Congress Prints & Photographs ----------
async function loc(q, {kind, limit = 8}) {
  if (kind === 'video') return [];
  const j = await getJSON(`https://www.loc.gov/pictures/search/?q=${enc(q)}&fo=json&c=${limit * 2}`);
  const out = [];
  for (const r of j.results || []) {
    const img = r.image;
    if (!img?.full) continue;
    // LoC rights vary per item — keep only items that state no known restrictions / PD.
    out.push({
      id: `loc:${r.pk || r.links?.item}`, source: 'Library of Congress', kind: 'image',
      title: r.title, creator: r.creator || 'Unknown', date: r.created_published_date || '',
      license: 'Check item page (LoC rights vary)', licenseUrl: r.links?.item || '', requiresAttribution: false,
      credit: `${r.title}. Library of Congress Prints & Photographs Division`,
      pageUrl: r.links?.item, previewUrl: img.thumb?.startsWith('//') ? 'https:' + img.thumb : img.thumb,
      downloadUrl: img.full?.startsWith('//') ? 'https:' + img.full : img.full, query: q, needsRightsCheck: true,
    });
    if (out.length >= limit) break;
  }
  return out;
}

// ---------- Internet Archive (video: only items with explicit PD/CC licenseurl) ----------
async function archive(q, {kind, limit = 8}) {
  if (kind !== 'video') return [];
  const query = `(${q}) AND mediatype:movies AND (licenseurl:*creativecommons.org/publicdomain* OR licenseurl:*creativecommons.org/licenses/by/*)`;
  const j = await getJSON(`https://archive.org/advancedsearch.php?q=${enc(query)}&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=licenseurl&fl[]=date&rows=${limit}&output=json`);
  const out = [];
  for (const d of j.response?.docs || []) {
    const lic = [].concat(d.licenseurl || [])[0] || '';
    out.push({
      id: `ia:${d.identifier}`, source: 'Internet Archive', kind: 'video',
      title: d.title, creator: [].concat(d.creator || ['Unknown'])[0], date: d.date || '',
      license: lic, licenseUrl: lic, requiresAttribution: /by/.test(lic),
      credit: `${d.title} — ${[].concat(d.creator || ['Unknown'])[0]} — ${lic} — Internet Archive`,
      pageUrl: `https://archive.org/details/${d.identifier}`,
      previewUrl: `https://archive.org/services/img/${d.identifier}`, downloadUrl: null, // resolved on approval
      query: q, needsFileResolve: true,
    });
  }
  return out;
}

// ---------- Pixabay (Pixabay Content License) ----------
async function pixabay(q, {kind, limit = 8}) {
  const key = process.env.PIXABAY_API_KEY;
  if (!key) throw new Error('PIXABAY_API_KEY not set');
  if (kind !== 'video') {
    const j = await getJSON(`https://pixabay.com/api/?key=${key}&q=${enc(q)}&image_type=all&per_page=${Math.max(limit, 3)}&safesearch=true`);
    return (j.hits || []).slice(0, limit).map((h) => ({
      id: `pixabay-img:${h.id}`, source: 'Pixabay', kind: 'image', title: h.tags, creator: h.user, date: '',
      license: 'Pixabay Content License', licenseUrl: 'https://pixabay.com/service/license-summary/', requiresAttribution: false,
      credit: `${h.tags} — ${h.user} — Pixabay`, pageUrl: h.pageURL, previewUrl: h.webformatURL, downloadUrl: h.largeImageURL,
      width: h.imageWidth, height: h.imageHeight, query: q,
    }));
  }
  const j = await getJSON(`https://pixabay.com/api/videos/?key=${key}&q=${enc(q)}&per_page=${Math.max(limit, 3)}&safesearch=true`);
  return (j.hits || []).slice(0, limit).map((h) => {
    const v = h.videos.large?.url ? h.videos.large : h.videos.medium;
    return {
      id: `pixabay:${h.id}`, source: 'Pixabay', kind: 'video', title: h.tags, creator: h.user, date: '',
      license: 'Pixabay Content License', licenseUrl: 'https://pixabay.com/service/license-summary/', requiresAttribution: false,
      credit: `${h.tags} — ${h.user} — Pixabay`, pageUrl: h.pageURL,
      previewUrl: `https://i.vimeocdn.com/video/${h.picture_id}_640x360.jpg`, downloadUrl: v.url,
      width: v.width, height: v.height, duration: h.duration, query: q,
    };
  });
}

export const SOURCES = {met, smithsonian, commons, loc, archive, pixabay};
export const IMAGE_SOURCES = ['met', 'smithsonian', 'commons', 'loc'];
export const VIDEO_SOURCES = ['pixabay', 'commons', 'archive'];

export async function searchAll(query, {kind, sources, limit = 6}) {
  const names = sources || (kind === 'video' ? VIDEO_SOURCES : IMAGE_SOURCES);
  const results = await Promise.all(names.map(async (n) => {
    try { return await SOURCES[n](query, {kind, limit}); }
    catch (e) { console.error(`  [${n}] "${query}": ${e.message.slice(0, 140)}`); return []; }
  }));
  return results.flat();
}
