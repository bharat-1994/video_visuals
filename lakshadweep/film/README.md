# Lakshadweep — Telugu documentary (film pipeline)

8-act, ~8.8 minute documentary built **entirely from code + free/open footage**:

| Layer | How it is made |
|---|---|
| Voice | your Telugu narration (`audio/*.mp3`) + word-level timestamps (`audio/*.timestamps.json`) |
| Picture | Python/OpenCV compositor (`render/`) — real NASA satellite imagery, Mixkit stock footage, CC-licensed photographs, and procedural animation (atoll formation, trade routes, flag, cyclone, sea-level…) |
| Subtitles | Telugu, burned in (mixed Telugu/Latin script shaping via HarfBuzz/Raqm) — `.srt` files in `out/` |
| Music + SFX | original score and sound design synthesised in numpy (`build/synth.py`, `build/score.py`), mixed with ducking + EBU R128 loudness (`build/mix.py`) |

## Outputs (`out/`)
- `Lakshadweep_Telugu_1080p24.mp4` — master (1080p, 24 fps, H.264 + AAC, -16 LUFS)
- `Lakshadweep_Telugu_720p_preview.mp4` — small preview
- `Lakshadweep_telugu.srt`, `Lakshadweep_english.srt` — subtitle files (for YouTube upload)
- `../CREDITS.md` — licences & attribution for every clip/photo used

## Rebuild
```sh
cd lakshadweep/film
sh build/fetch_maps.sh                  # NASA GIBS imagery (public domain)
python3 build/parse_audio.py            # voice alignment -> build/segments.json
python3 build/score.py                  # music + environment sfx stems   (~4 min)
python3 build/sfx_trans.py              # transition whooshes from the edit
python3 build/mix.py                    # voice + music + sfx -> build/out/master.wav
python3 render/render_parts.py 4 20 20  # parallel 1080p render (workers, chunk seconds, crf)
python3 build/final.py                  # mux -> out/*.mp4
python3 build/make_credits.py           # SRTs + CREDITS.md
```
Footage from Mixkit and Flickr is downloaded on first use (`render/assets.py`, `build/mixkit_lib.py`).

## Edit structure
`render/act1.py … act8.py` list every cut with its act-local time (aligned to the narration), transition and grade.
Preview any act as a contact sheet: `python3 render/preview.py 3 2`.
