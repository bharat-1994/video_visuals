# 06 — Production, review & QA

## 6.1 Principles
1. **Work in phases with gates.** Each phase produces evidence you (and the user) can see.
2. **Make things cheap to redo.** Chunked, resumable rendering; per-act files; hashed caches.
3. **Look and listen at every stage** — before the expensive step.
4. **Tell the user the truth** about what is real/stock/generated/uncertain.
5. **Keep a decision log** so any other model or person can continue consistently.

## 6.2 Phases and gates

| Phase | Output | Gate (must pass) |
|---|---|---|
| 0 Brief | `brief.md` (topic, audience, length, languages, licences, output, dials, identity line) | User confirms or accepts defaults |
| 1 Outline & script | outline, `script.md`, `narration_only.md`, fact table | User approves tone/length; facts graded |
| 2 Voice | audio per act + word/char timestamps + text/translation | All text lines located in the alignment |
| 3 Timeline | master timeline table | Acts and gaps look right |
| 4 Assets | candidates, contact sheets, chosen assets, honesty matrix | Every beat has a rung + backup |
| 5 Edit plan | beat table + per-act shot list | Reviewed contact sheets of every act |
| 6 Sound plan | music brief, per-act composition table, bed curves, cue sheet | Plan matches the shot list |
| 7 Build audio | stems + master wav | Loudness numbers, level table, listen test |
| 8 Render | picture chunks → silent video | No failed chunks; duration matches |
| 9 Mux & deliverables | master, preview, subtitles, credits | Final QA below |
| 10 Handoff | delivery note, decision log | User has files + honest notes |

## 6.3 Working with the user (collaboration protocol)

### 6.3.1 Ask a few questions, once, with defaults
1. Visual sourcing (free downloads / own library / AI credits).
2. Captions (burned subs / minimal titles / none).
3. Output spec (1080p24 default; 4K; vertical).
4. Music & SFX source (original/synthesised, supplied, placeholder).
5. Constraints (people, brands, politics, places not to show).

### 6.3.2 Show evidence at each gate
- Printed tables (timeline, level table).
- Contact sheets (images you looked at) — describe what you saw and what you'll fix.
- Numbers (LUFS, true peak, counts).

### 6.3.3 Report honestly
- Distinguish: **done and verified** / **done, not verified** / **not done**.
- Surface deviations and compromises (e.g., "stock beach footage used for mood").
- If something external fails (rate limits, missing assets), say so and say what you substituted.

### 6.3.4 Deliverables
- Master video, small preview (+ share-friendly version if files are large), subtitle files (native + translation), credits, handoff note. Provide **download paths and instructions**; think about how the user will actually get the files (file size limits, hosting).

## 6.4 Making the render robust

### 6.4.1 Chunked, resumable, parallel
- Split the timeline into **20-second chunks** (`part_000.mp4…`); each chunk is independent.
- Render chunks in parallel (one per core); write to `.tmp` and rename on success; skip existing parts when resuming.
- Concatenate losslessly (`-c copy`).
- Catch exceptions per chunk and report `FAILED` instead of crashing the pool.
- To fix one shot: delete the affected chunk(s) and re-run; only those re-render.

### 6.4.2 Memory & performance
- Build shots lazily; release finished shots; avoid keeping all frames/arrays alive.
- Vectorise per-frame math; keep scenes < ~1.5 s/frame on CPU; pre-compute noise banks, masks and LUTs.
- Pipe raw frames to the encoder (`rgb24 → libx264 -crf 18–20 -preset fast`).
- Typical cost: 8–9 min 1080p24 on 4 cores ≈ 30–40 minutes wall time.

### 6.4.3 Long-running commands in constrained shells
- Run long jobs in the background and poll their logs; use notifications/monitors rather than blind `sleep`.
- Keep each foreground command under the tool's timeout.

## 6.5 Review passes (do them in this order)

### Pass A — Plan review (before building)
- Read the beat table aloud with the narration. Does each picture explain its line?
- Check the three signature transitions; check the identity line.

### Pass B — Contact-sheet review per act (cheap, mandatory)
Render **2 frames per cut** (with subtitles and overlays) into a sheet per act. Inspect for:
- wrong/blank/black frames; clipped whites; muddy colours;
- watermarks or text;
- composition under subtitles;
- repeated clips; adjacent similar frames;
- overlays out of place; labels overlapping;
- mismatched transitions (two unrelated frames blended).

### Pass C — Silent pass (final)
Play the film with sound off. Does it tell a coherent, varied story? Any dead stretches?

### Pass D — Audio-only pass
Close your eyes. Does voice + sound feel complete? Any jumps, clicks, tonal clashes?

### Pass E — Technical scans (automate)
- **Durations:** video duration = audio duration (±1 frame).
- **Black-frame scan:** list intervals where mean luminance < threshold; only chapter gaps/ends/deliberate beats allowed.
- **Subtitle overlap scan:** no windows overlap; no line > 2 rows.
- **Loudness:** integrated −16 ±0.5 LUFS; TP ≤ −1.5 dB; LRA 8–12 LU.
- **Level profile:** 5-second RMS list within ±2–3 dB (except intended dips).
- **File integrity:** playable (ffprobe), correct codec/pixel format, `faststart`.

### Pass F — Final contact sheet
Sample 1 frame per 6–8 s of the final file → one big sheet. Check order, variety, pacing, subtitles.

### Pass G — Honesty and legal
- Credits complete; licences recorded.
- Disclosures (real/stock/generated/legend).
- Facts list (verify before publishing).

## 6.6 Metrics worth recording (for improvement)
- Average shot length and distribution.
- Count of: transitions by type, SFX cues per act, procedural scenes, text overlays.
- % of runtime by rung (draw / real / still / mood).
- Loudness numbers; peak; LRA.
- Render time per chunk.

## 6.7 The decision log (keep it as you go)
One line per major decision:
```
[phase] Decision — reason (the line/idea it serves) — alternatives rejected
```
Example: `[edit] Used whip transition on "3 questions" — rapid topic jump, answers question set-up — rejected iris (reserved for scale reveal)`.
This is the real "thought process" artifact; hand it to any model that continues the work.

## 6.8 Handoff / delivery note template
- What you delivered (files, sizes, specs).
- What is real / stock / generated / legend.
- Facts to verify.
- Known compromises & how to improve them (e.g., "replace shots X, Y with local footage").
- How to re-render a single act.
- Licences & credits location.

## 6.9 Common process failures
| Failure | Prevention |
|---|---|
| Audio re-recorded → timing lost | Keep beat table keyed to line text; re-run alignment, re-derive times |
| Last-minute asset change breaks continuity | Resumable chunks + per-shot factories |
| Subtle bugs only visible at full res | Final spot checks at 1080p, not only thumbnails |
| Overbuilt effects | Review pass C — remove what you notice |
| Download blocked late | Front-load downloads; have backups |
| Delivery inaccessible to the user | Plan file size/hosting early; offer split/hosted/smaller versions |
