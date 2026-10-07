# 01 — Story & script

## 1.1 Principles
1. A documentary is an **argument told as a journey**. Before any research list, write the *promise*: one sentence the viewer should believe at the end.
2. **Every act has exactly one job.** If you can't state the job in 6 words, the act is two acts or none.
3. **The first minute earns the rest.** Open with a puzzle or a corrected misconception, not with "Welcome to…".
4. **End by echoing the opening**, changed. The viewer should feel the film close like a circle.
5. **Spoken language is not written language.** Write for the ear: short, rhythmic, one idea per line.
6. **Certainty has three grades** (fact, widely told story, legend). Mark them in the words, not in footnotes.

## 1.2 Decision procedure: from topic to structure

### Step A — The promise
Template: *"After this film the viewer will believe/feel ______ because ______."*
Lakshadweep: *"A tiny, fragile place exists because of tiny creatures and careful people — and its future depends on that same care."*

### Step B — The shape
Pick a story shape; adapt it. Reusable shapes:

| Shape | Sequence | Use when |
|---|---|---|
| **Place biography** (used here) | puzzle → origin → people → power/history → daily life → threats → lesson | A place, region, institution |
| **Mystery** | question → clues → false answer → real answer → implication | Science/history puzzles |
| **Process** | goal → ingredients → steps → failure points → result | How something is made |
| **Rise & fall** | ordinary world → breakthrough → peak → cause of decline → legacy | Companies, empires |
| **Three questions** | pose three → answer each → combine | Explainers (we also used this as the Act-1 promise) |
| **Day-in-the-life** | dawn → work → crisis → rest → night | Communities, jobs |

### Step C — Acts
Aim for 6–9 acts of 45–80 s each for a 8–10 min film (shorter acts feel restless; longer acts need sub-turns).

Act design card:
```
Act N — Title (internal, never spoken)
Job:        (6 words)
Temperature: calm / curious / tense / hopeful / reflective
Opening line type: hook / bridge / question
Key turn:   the sentence where the act changes direction
Exit:       how it hands to the next act (question, contrast, calm)
Facts used: (list) + certainty grade for each
```

### Step D — Emotional temperature curve
Write one word per act. Rules of thumb:
- Never two tense acts back to back; insert a breath.
- The most tense act sits at ~75% of the film.
- The last act is reflective-warm, not triumphant.

Lakshadweep curve: 1 curious → 2 wonder → 3 reverent/curious → 4 tense/ambivalent → 5 suspenseful→proud → 6 warm/joyful → 7 worry→hope → 8 reflective.

### Step E — Hook & echo
Hook that corrects a misconception: *"Lakshadweep means 'a lakh of islands' — there are 36."* The film's last act returns to the *name* (and the tiny creature) so the circle closes.

## 1.3 Writing narration for the ear (and for TTS)

### Rules
- **One idea per sentence.** If a sentence has two verbs doing separate things, split it.
- **Length:** 4–16 spoken words typical; allow a few 20-word sentences for flow; use 2–4-word sentences for punch ("But the truth is different.").
- **Rhythm pattern:** long–short–short, or question–pause–answer. Avoid five long lines in a row.
- **Numbers:** write them how a person says them; avoid long numerals; round when precision doesn't matter ("almost four lakh square kilometres").
- **Comparisons beat statistics:** convert a number into a thing viewers know ("not even one-twentieth of Hyderabad").
- **Questions** pull viewers; use 3–6 per film.
- **No stage directions** in the narration file. Keep visual notes in a separate file.
- **Punctuation is pacing:** `.` = full stop; `…` = longer hold; `,` = micro-pause; dashes read inconsistently in TTS — avoid.
- **Pronunciation:** foreign words either spelt as spoken or kept in the original script that the TTS handles well; test a 10-second sample first.
- **Avoid:** jargon without a plain restatement; stacked clauses; "in conclusion"; rhetorical drama ("breathtaking", "unbelievable").

### Tone calibration
Calm, curious, a little warm — "a friend explaining something they find fascinating". If you notice adjectives doing the work, replace them with a concrete fact.

### Code-mixed conversational narration (Telugu example; adapt to any language)
- Mix English only for **terms people really say in English** (coral, lagoon, erosion, climate change, tourism, permit). Don't force English for emphasis.
- Keep English words in Latin script in the script file if the TTS handles them; otherwise transliterate and test.
- Use direct address sparingly ("మీరు… ") and inclusive "we" for exploration ("ఇక మొదలు పెడదాం" = "let's begin").
- Use the natural spoken contractions of the language, not literary forms.
- For legends: *"…అని నమ్మకం", "…అంటారు", "ప్రచారంలో ఉన్న కథనం ప్రకారం…"* — "according to belief / it is said / the popular account". The viewer hears the hedge.

## 1.4 Handling uncertainty and facts
1. Collect facts in a table: *claim | source | certainty grade (A fact / B widely reported / C legend or contested)*.
2. **A** = state directly. **B** = attribute ("according to…"). **C** = narrate as story with explicit hedge *and* never visually "prove" it (no fake documents, no recreations that look like footage).
3. Provide a "verify before publishing" list in the delivery (numbers, dates, population shares).
4. If two sources disagree, either use the safer claim or present as range.
5. Don't invent quotations, dialogue, or precise times.

Lakshadweep examples:
| Claim | Grade | How narrated | Visual handling |
|---|---|---|---|
| 36 islands, 10 inhabited | A | direct | counted dots on real map |
| Ridge/coral atoll formation | A | direct | schematic cross-section (clearly diagrammatic) |
| Saint Ubaidullah arrival (7th c.) | C | "according to the belief of the local people" | map pin + dusk imagery; no "historical" visuals |
| Portuguese poisoned at Androth | C | "popular narrative… difficult to say whether story or history" | mood footage, silhouettes; no reconstruction as fact |
| 1947 flag story | B/C | "widely circulated story… it is said" | animated routes and a flag on a beach — symbolic, not archival |
| 2016 bleaching, 2017 cyclone | A | direct | satellite imagery, stock reef footage (disclosed) |

## 1.5 Script production loop
1. **Outline** (acts + job + key turn) → user approves.
2. **Draft** in the user's language; keep a plain-English gloss file for your own checking.
3. **Read aloud test:** can each line be said in one breath? Mark any that can't.
4. **Trim**: remove 10–15% — every draft is longer than it needs to be.
5. **Produce `narration_only.md`**: no headings, no stage directions → feed to TTS or the voice artist.
6. **After audio exists**: re-time everything from the *actual* audio (chapter 02). Never assume your word-count estimate.

## 1.6 Checklist (script)
- [ ] Promise sentence written and every act serves it.
- [ ] Each act: one job, one key turn, handoff.
- [ ] Hook corrects a misconception; last act echoes the first.
- [ ] Temperature curve has no tense–tense adjacency.
- [ ] Every number and date is in a verify list with a grade.
- [ ] Legends hedged in the words.
- [ ] No sentence needs a visual note to make sense (picture adds, doesn't rescue).
- [ ] TTS-ready file has no headings/directions.
