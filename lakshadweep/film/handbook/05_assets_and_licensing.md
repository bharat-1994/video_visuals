# 05 — Assets, sourcing & licensing

## 5.1 Principles
1. **Look before you choose.** Never choose clips from titles; build contact sheets and read them.
2. **Respect licences.** Know what each source allows; keep a machine-generated credits file.
3. **Honesty.** Do not present stock as the real place; disclose real vs stock vs generated.
4. **Prefer real data** (satellite, archives) over generic stock where the story is about a specific place.
5. **Be polite to servers** (rate limits, user-agents, retries) — and have fallbacks.
6. **Cache everything locally**; conform once.

## 5.2 What kinds of assets you need (per film)
| Type | Examples | Typical share |
|---|---|---|
| Data imagery | satellite, bathymetry, night lights, maps | 25–35% (geographic films) |
| Procedural/diagram | animations you generate | 20–30% |
| Real footage | the place, people, events | as available |
| Mood footage | water, sky, light | ≤25% |
| Real stills | local photographs, archives | 10–20% |
| Typography/overlays | titles, tags, subtitles | tiny |

## 5.3 Source catalogue (what we used and how)

### 5.3.1 NASA GIBS (Global Imagery Browse Services) — public domain
- **Use:** whole-Earth to 30 m imagery; bathymetry; night lights; storm imagery.
- **How:** WMS GetMap (EPSG:4326). Choose layer, time, bounding box, size.
  - Relief + bathymetry: `BlueMarble_ShadedRelief_Bathymetry` (no time)
  - True colour daily: `MODIS_Terra_CorrectedReflectance_TrueColor`, `MODIS_Aqua_…`, `VIIRS_SNPP_CorrectedReflectance_TrueColor`
  - 30 m: `HLS_S30_Nadir_BRDF_Adjusted_Reflectance` (choose a clear date; small boxes ≈ 0.2–0.4° wide for islands)
  - Night lights: `VIIRS_Black_Marble`
- **Tips:** request ≥ 2× the final needed resolution; choose clear-sky dates by trial (scan several dates); stack several scales; enhance (gamma 0.7–0.9, saturation ×1.2, lift deep blues, unsharp mask); fill isolated black pixels; colour-match layers.
- **Acknowledgement text:** "We acknowledge the use of imagery provided by services from NASA's Global Imagery Browse Services (GIBS), part of NASA's Earth Observing System Data and Information System (EOSDIS)."

### 5.3.2 Stock footage with permissive licence (e.g., Mixkit)
- **Use:** mood footage, general-world shots.
- **How:** crawl category pages → collect clip ids and slugs; download 360p previews; build contact sheets with ids burned in; choose; then fetch HD.
  - Direct file URLs follow patterns (older ids: `/videos/{id}/{id}-1080.mp4`) or are in the page's structured data (`contentUrl`, `embedUrl`).
- **Check the licence page** of the provider; credit anyway.

### 5.3.3 Community archives (Wikimedia Commons, Internet Archive)
- **Use:** local photographs, historical images, scientific footage, public-domain government footage.
- **How:** search API for *titles + licences*; for bulk download be gentle (descriptive User-Agent, delays, honour `Retry-After`; 429s can last 10 minutes).
- **Licence details:** per file (CC0, CC BY, CC BY-SA, public domain, government open licences) — record each.

### 5.3.4 Openverse → Flickr (CC)
- **Use:** local photographs of places that Commons lacks.
- **How:** Openverse search (≤20 results per request anonymously), filter licences (CC BY, CC BY-SA, CC0), keep creator, title, URL.
- **Avoid** NC/ND if the project may be monetised/modified.

### 5.3.5 Government open data (NOAA, NASA media, national archives)
- Often public domain or open licence; verify per item.

### 5.3.6 Generated imagery (optional)
Only with explicit credits/approval; keep a consistent style prompt; label as generated; never to fake a specific real place.

### 5.3.7 Music & sound sources
- Synthesise (this film), commission, or license (royalty-free libraries). Keep licence text in the credits file.

## 5.4 Evaluating candidates (the look-first method)
1. Build a **candidate catalogue** (id, title, size, licence, URL).
2. Download small previews/thumbnails.
3. **Contact sheets**: 2–4 frames per clip, id burned in, ~20 per sheet.
4. Read every sheet. Mark: keep / maybe / reject, with notes (e.g., "good for dusk mood", "logo visible", "wrong place").
5. Rank by: truthfulness → emotional fit → technical quality → variety.
6. Download HD only for the keepers.

### Technical quality checks
- Resolution ≥ 1080p (or high enough for the planned push).
- Frame rate (conform later), interlacing, compression artefacts.
- Camera shake that would fight your motion.
- Colour cast that would be hard to grade.
- Watermarks/logos/captions; faces that need consent.

## 5.5 Honesty matrix (create one per film)
| Shot | Type | Is it the place? | Disclosure |
|---|---|---|---|
| Satellite map | Real data | Yes | credited |
| Atoll cross-section | Diagram | n/a | labelled schematic in delivery note |
| Fishing at dusk (stock) | Stock | No | disclosed |
| Beach photos | Real still | Yes | CC credits |
| Silhouette ships | Illustration over stock | n/a | marked as legend illustration |

## 5.6 Licensing hygiene
- Maintain `CREDITS.md` generated from the shot list (ids → licence + creator + link).
- CC BY / BY-SA require attribution: put in video description or credits file; mention BY-SA obligations.
- Do not scrape pages that forbid it; use official APIs/downloads where available; keep request rates low.
- Keep original files unchanged; derived files get new names.
- If a licence is unclear → do not use.

## 5.7 Handling rate limits and failures
| Symptom | Response |
|---|---|
| HTTP 429 (Commons) | Wait `Retry-After`, then slow; use alternate sources; front-load downloads early in the project |
| 403 from a stock site's HTML | Use official file URLs/APIs |
| Broken partial downloads | Download to `.part`, rename on success |
| Provider offline | Have 1–2 alternates per beat |
| Poor-quality asset chosen | Re-open contact sheet; replace; re-render only the affected part |

## 5.8 Caching & conforming
- One folder per source type; cache previews separately from HD.
- **Conform cache:** each (source, start, duration, speed, filter) → 1080p/24 fps H.264 (high quality, crf ≈ 13). Hash the parameters so re-renders reuse them.

## 5.9 Checklist (assets)
- [ ] Every beat has a primary and a backup asset.
- [ ] Contact sheets reviewed; notes saved.
- [ ] Licences recorded; credits generated.
- [ ] Honesty matrix written.
- [ ] Rate-limit-sensitive downloads done early.
- [ ] Conformed cache built.
