# 07 — Templates (copy, fill, show to the user)

Each template is a small file/section you create during the project. Filling them *is* the thinking; the production follows from them.

---

## T1. Brief (`brief.md`)
```
# Film brief
Title (working):
Topic & scope:
Promise (one sentence — "After this film the viewer will believe/feel ___ because ___"):
Audience & context (platform, age, prior knowledge):
Tone (3 adjectives; and 3 words to avoid):
Length target / act count:
Narration language(s) & register (formal / conversational / code-mixed):
Subtitles: languages, burned-in or separate:
Output spec: resolution, fps, aspect, loudness target:
Sourcing allowed: free downloads / own library / AI credits / commissions:
Licences allowed (e.g. CC BY OK? CC BY-SA OK? NC no):
Do-not-show list (people, brands, politics, places, images):
Deliverables:
Deadline / compute budget:
```

## T2. Identity line & dials (`identity.md`)
```
Identity line (one sentence a stranger could picture):
   e.g. "Calm, turquoise, tanpura + bansuri + frame drum, whip only for questions."

Dials (decide from the TOPIC's place/culture/emotion; write the reason):
- Palette: hero / accent / signal / history —
- Pace: avg shot length, distribution —
- Signature transitions (3) + chapter dip —
- Music world: tonic & mode / lead instrument / rhythm feel / palette (≤6 timbres) —
- Motif idea & its transformations —
- Title style (typeface pairing, spacing, placement) —
- Procedural scene set (3–8 scenes this topic needs) —
- Text density: —
- Sound design density: —
- Opening image / closing image: —

Compared with the previous film: identical dials: ___ (if >2 identical, change them)
```

## T3. Fact table (`facts.md`)
| # | Claim | Source | Grade (A fact / B widely reported / C legend/contested) | How narrated | Visual handling |
|---|---|---|---|---|---|

## T4. Act design card
```
Act N — internal title
Job (6 words):
Temperature (calm/curious/tense/hopeful/reflective):
Hook / bridge / question opening:
Key turn (sentence):
Exit (handoff):
Facts used (#s):
```

## T5. Beat table (`beats.csv`) — the central edit document
```
act, beat_id, start_s (act-local), end_s, narration_gloss, idea, visual_rung(1-5), asset_or_scene, motion, transition_in, grade, sound_notes, why
```
Example rows:
```
1,b03,6.26,8.84,"There are a total of 36 islands",count,1,"satellite dive + 36 dots","camera dive; dots stagger 0.07s",dissolve,teal,"soft ping on each dot cluster","a count → show countable things"
1,b05,18.50,22.07,"not even one-twentieth of Hyderabad",comparison,1,"city night lights + 20 squares","slow push",iris,warm,"low whoosh under iris","comparison viewers can feel"
```

## T6. Shot list line (code or editor note)
```
[act.local_time] name | transition (duration) | grade | asset/scene | motion | text overlay? | why (one line)
```
Rules: *why* must reference the idea, not the image ("shows loss", not "pretty reef").

## T7. Asset candidate log (`assets.md`)
| id | source | URL | licence | creator | what it shows | rung | keep/maybe/reject | notes (logos, watermark, mood, colour) |
|---|---|---|---|---|---|---|---|---|

## T8. Honesty matrix (`honesty.md`)
| Shot/Beat | Type (real data / real footage / real still / stock mood / diagram / generated / legend illustration) | Is it the place? | Disclosure text |
|---|---|---|---|

## T9. Music brief (`music_brief.md`)
```
World:
Palette (≤6 timbres):
Tonic / mode / tempo range:
Motif (contour + rhythm) & transformations:
Mood arc per act (one word each):
Hit points (act, time → event):
Rests (where music stops):
Dynamics policy (voice-relative):
Avoid:
References (moods, not tunes):
```

## T10. Per-act composition table
| Act | Mood | Chord loop (8 s per chord) | Motif use | Rhythm (where, bpm) | Hit points | Rests | Reverb sends |
|---|---|---|---|---|---|---|---|

## T11. Bed levels (automation sketch)
| Time | Ocean/room | Wind | Special bed (underwater, rain…) | Notes |
|---|---|---|---|---|

## T12. SFX cue sheet
| time | on-screen event | sound | pan | level (rel. voice) | reverb | variant/notes |
|---|---|---|---|---|---|---|

## T13. Level table (after the first mix)
| Act | Voice (dB RMS) | Music (pre-duck) | Bed+SFX | After duck: music during speech | Notes |
|---|---|---|---|---|---|

## T14. QA report (`qa.md`)
```
Plan review:            pass/fail + notes
Contact sheets (per act): pass/fail + defects + fixes
Silent pass:            notes
Audio-only pass:        notes
Durations (video/audio): __ / __
Black-frame scan:       intervals + justification
Subtitle scan:          overlaps / >2 lines
Loudness:               I=__ LUFS, TP=__ dBTP, LRA=__ LU
Level profile:          min/max 5-s RMS
File check:             codec, fps, size, faststart
Final contact sheet:    notes
Honesty/legal:          credits ok? disclosures ok?
Open issues:
```

## T15. Decision log (running)
```
[YYYY-MM-DD] [phase] decision — because (idea/line) — rejected alternatives
```

## T16. Delivery note (to the user)
```
Delivered: files, sizes, specs.
What is real / stock / generated / legend: (table summary)
Facts to verify: (list)
Compromises & suggested upgrades: (list)
How to re-render a single act:
Where credits/licences are:
How to download/host (size constraints):
```

## T17. Prompt for a new LLM (kick-off)
```
You are the director, editor, composer and sound designer of a documentary.
Read the handbook (00–09). Follow chapter 06's gates and chapter 09's quality bar.
Topic: {topic}. Language: {language}. Length: {minutes}. Audience: {audience}. Tools: {tools}.
First produce T1 (brief), T2 (identity & dials — compare with previous film if any), T3 (facts), and an outline with T4 cards.
Stop and show me these. After approval, continue phase by phase, filling the templates and showing evidence at each gate.
Keep a decision log (T15). Be honest in the delivery note (T16).
```
