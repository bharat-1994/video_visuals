# Test brief — 3 shots (≈12 s)

Topic: Elon Musk, 2008. New shots — none of these exist in `examples/`.
Write `test_shots.py` (and `test_assets.py`) defining:

```python
SCENES = [(4.0, shot1), (4.2, shot2), (4.6, shot3)]
CUES   = [...]          # (shot_id, t_seconds, "sfx_name", gain_db)
SUBS   = ["...", "...", None]   # narration subtitles; None for the dialogue shot
```

## Shot 1 — landmark + action (tests asset recognizability)
Narration/subtitle: "September 2008. Falcon 1, attempt number four."
Staging: Omelek Island, Kwajalein Atoll (Marshall Islands): a tiny flat tropical island, white sand, a few palm trees,
turquoise lagoon and deep-blue ocean around it. On the island: a small launch pad with a thin service tower and
the Falcon 1 rocket — a slim, tall, white/silver two-stage rocket, black interstage band, pointed fairing, single
engine. Caption "Sept 2008 · Omelek Island" typewritered top-left. At ~2.2 s the rocket lifts off: flame, a growing
smoke cloud at the pad, the rocket climbing out of frame top; camera pushes slightly. Signature features to check:
slim rocket proportion (~15:1), black band, island tiny in a big ocean, palms.

## Shot 2 — staging + hands (tests physical common sense)
Narration/subtitle: "Three rockets had failed. The money was almost gone."
Staging: night, small cluttered office. elon_adult sits side-on at a desk (facing right), laptop on the desk OPEN
and FACING HIM (we see the back of the lid), his left hand holding a phone to his ear (`phone_R`-like pose on the
correct side), right hand on the laptop. A stack of envelopes marked "OVERDUE" grows by popping in, one at a time.
A wall chart with three red X's (one per failed launch). Mug, desk lamp. Expression: worried → tired.

## Shot 3 — dialogue (tests characters, lip-flap, text placement)
Dramatized dialogue (make clear by context that it's illustrative):
- Investor (new character you design with `Puppet(...)`: grey hair, glasses, suit) facing left, across a table: "Three failures. Why fund a fourth?" (t≈0.3–2.0, talking)
- elon_adult facing right: "Because the fourth one flies." (t≈2.2–end, talking)
Meeting room, window with city, a flip chart with a rocket sketch. Investor's expression skeptical (smug/worried);
Elon determined. Keyword "Attempt #4" may pop at the end.
