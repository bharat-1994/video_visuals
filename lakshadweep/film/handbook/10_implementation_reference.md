# 10 — Implementation reference (this repo's code, as one possible toolchain)

Everything in chapters 01–09 is tool-agnostic. If you want to use the same Python/ffmpeg toolchain, this is the map. (Environment used: Linux, 4 CPU cores, no GPU; python3, numpy, scipy, opencv, Pillow with Raqm/HarfBuzz, ffmpeg with libx264/libass.)

## Folder map
```
audio/                    voice mp3 + char-level timestamps json + text/translation txt (inputs)
assets/                   fonts, maps (NASA), flickr stills table, mixkit cache (git-ignored heavy files)
build/                    audio & asset tooling
render/                   picture engine + per-act edit lists
out/                      deliverables (srt, mp4 git-ignored); final/ (LFS)
handbook/                 this documentation
```

## Build scripts (`build/`)
| File | Purpose |
|---|---|
| `parse_audio.py` | Locate each text line in the char-timestamp stream → `segments.json` |
| `timeline.py` | Master timeline: act start times, pre-roll 5 s, gap 1.6 s, outro 10 s |
| `synth.py` | DSP primitives: filters, noise, instruments (tanpura, pad, piano, bell, flute, drums), riser, ocean, wind, gull, thunder, rain, creak, reverb IR + convolution |
| `score.py` | Composition + sound design on the master timeline → `music.npy`, `sfx.npy` |
| `sfx_trans.py` | Transition whooshes generated from the actual edit → `trans_sfx.npy` |
| `mix.py` | Voice chain, normalisation, ducking, soft limiter, two-pass loudnorm → `master.wav` |
| `final.py` | Mux video+audio → master mp4 + 720p preview |
| `make_credits.py` | SRTs (native + English) + `CREDITS.md` from the shot list |
| `fetch_maps.sh` | NASA GIBS WMS downloads |
| `prep_maps.py`, `match_layers.py` | Enhance satellite imagery; colour-match layers via low-frequency transfer |
| `mixkit_*`, `catalog*.py`, `commons.py`, `ov.py`, `fetch_all.py` | Asset discovery and polite downloading (Mixkit, Commons, Openverse) |

## Render engine (`render/`)
| File | Contents |
|---|---|
| `engine.py` | `Shot` classes (VideoShot, StillShot, FuncShot), transitions (`TRANS`: dissolve, dip, whip, zoom, flare, iris, luma, cut), `GRADES` + `grade()`, finishing (bloom/vignette/grain), titles/tags/subtitles (mixed-script runs), `Entry`, `Timeline`, `write_range` |
| `geo.py` | `Layer`, `GeoView` (multi-resolution satellite stack with feathered masks), `cam_path` (log-zoom easing), overlays: `marker_overlay`, `path_overlay`, `label` |
| `fx.py` | particles, god rays, caustics, light leak, fades |
| `shots.py` | factories: `vid()`, `img()`, `func()`, `solid()`, effect helpers (`dust`, `rays`, `caust`, `fade_in/out`), watermark-crop list |
| `assets.py` | resolve assets: Flickr table, Mixkit ids (`mk:ID`), conform cache (hash-keyed, 1080p/24) |
| `film_core.py`, `film.py` | `cut()`, `tag()`, timeline build, act dips |
| `scenes_a1.py`, `scenes_a2.py`, `scenes_misc.py` | content-specific procedural scenes (dot cloud, city-grid, EEZ, cross-sections, routes, flag, cyclone, sea-level, matrilineal, split-wipe, heat map, cable map, silhouettes) |
| `act1.py … act8.py` | the edit: one `cut(act, local_time, factory, transition, duration, grade, name)` per beat |
| `preview.py` | contact sheets per act (with subtitles/overlays) |
| `render_parts.py` | parallel, resumable 20-second chunk renderer + lossless concat |

## Typical command sequence
```sh
python3 build/parse_audio.py
python3 build/timeline.py
sh build/fetch_maps.sh
python3 render/preview.py 3 2          # review each act
python3 build/score.py                 # ~4 min
python3 build/sfx_trans.py
python3 build/mix.py                   # master.wav at -16 LUFS
python3 render/render_parts.py 4 20 20 # parallel render
python3 build/final.py                 # mux + preview
python3 build/make_credits.py          # srt + credits
```

## Conventions
- Time in seconds; act-local times in the act files; `GT(act, local)` → global.
- Grades are named presets; transitions are named; every cut has a `name` for debugging and the preview sheet.
- Heavy outputs are git-ignored; delivery uses LFS or hosting.

## Adapting to another film (code route)
1. Replace `audio/` inputs; re-run `parse_audio.py`; edit `timeline.py` if needed.
2. Write new `act*.py` from your beat table; write new procedural scenes for the new content (reuse `geo.py`, `fx.py`, `engine.py` as libraries).
3. Rewrite the compose part of `score.py` from your music brief; keep `synth.py` primitives or add new instruments.
4. Reuse `mix.py`, `render_parts.py`, `final.py`, `make_credits.py` unchanged.
