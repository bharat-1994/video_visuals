# Vietnam film: state

**Status:** full film built (151 shots, 10:09). Narration: 12 TTS parts joined in `narration.wav` (0.3 s gaps); word timings in `words.json`.

## How it is built
- `film.py`: one line per shot in the scene mini-language (`engine/scene.py`). Shot cuts come from `shots.json` (Act 1a, S01–S15) and `segs.json` (S16–S151, auto-cut at clauses and then hand-fixed).
- `key.py`: hand-coded key shots S01, S12, S14 and S15.
- `film_setup.py`: registers backgrounds, cast, assets and custom shot code (zone, mill, stamp, price line, gauge, map pins, Asia map, pie, cage lift).
- Assets: `assets.py` (director: cast, map, cage, ration props), `assets_ind.py` (Sonnet: industry/tech), `assets_pol.py` (Sonnet: policy/story).
- Sounds are automatic: pop on every pop-in, ticks on counters and typewriter text, a thud on shakes, an ambience bed per background, plus explicit `sfx` items.

## Commands (run from the kit root)
```
SHOTS=S20,S21 python3 engine/sheet.py episodes.vietnam.film s.jpg    # preview some shots
python3 engine/build.py episodes.vietnam.film vietnam.mp4            # full film with narration + SFX + music
```

## Motifs
- The gold map is caged in S12 (EMBARGO), propped up by the USSR pillar in S14 and loses that prop in S15.
- The cage lifts off in S65 (1994) and again as the callback in S146.
- The golden key (ownership) is planted in S133 and pays off in S149 and S151.

## Open
- The Qwen batch B01 attempt failed. Act 1 was rebuilt here in the mini-language instead.
