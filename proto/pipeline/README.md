# Script-to-video pipeline

Real stock footage and public-domain art only. No generated visuals. Only approved clips are ever saved.

| # | Step | Who/what | Output |
|---|------|----------|--------|
| 1 | Write the script | you | `projects/<p>/beats.json` → `script` |
| 2 | Split into beats + keywords | Claude (in session) | `beats.json` → `beats[]` (`text`, `visual`: image/video/map, `queries`, `exclude`) |
| 3 | Find candidates | `node pipeline/search.mjs projects/<p>` | `candidates/candidates.json`, `candidates/contact_sheet.html` (thumbnails only; source, license, credit per item) |
| 4 | **You approve** | you | `approvals.json` — `{ "b1": [{"id": "...", "as": "file.jpg", "start": 296, "duration": 8, "crop": "w:h:x:y"}] }` |
| 5 | Save chosen clips + ledger | `node pipeline/fetch.mjs projects/<p>` | `public/<p>/*`, `credits.json`, `CREDITS.md` |
| 6 | Voiceover + timings | ElevenLabs (speech, then scribe for word timings) → `audio/mix.sh` | `public/<p>/mix.mp3`, `src/<p>-words.json` |
| 7 | Render | a Remotion composition per project (see `src/RoeScene.tsx`) → `npx remotion render src/index.ts <Id> renders/<p>.mp4` | mp4 |

Sources (`lib/sources.mjs`): Met, Smithsonian Open Access, Wikimedia Commons, Library of Congress, archive.org (explicit PD/CC items only), Pixabay (needs `PIXABAY_API_KEY`).
License rules: Met/Smithsonian CC0; Commons accepts only PD/CC0/CC BY/CC BY-SA and flags attribution; LoC items need a manual rights check (`rightsVerified: true`); previews are cached, full assets are fetched only on approval.
Video from remote sources is cut with ffmpeg range requests, so long sources are never fully downloaded.
