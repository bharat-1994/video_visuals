# The Documentary Handbook (exhaustive, tool-agnostic)

Everything that went into the Lakshadweep film, written so that **any capable LLM or human**, with **any toolset**, can reproduce the *quality* — and make a film that has its *own* identity.

How this handbook is organised: each chapter has **(a) principles** (why), **(b) decision procedures** (how to choose), **(c) concrete defaults and ranges** (numbers you can start from, with the reasoning, so you can deviate intelligently), **(d) checklists**, and **(e) examples from the Lakshadweep film**.

| # | Chapter | Answers |
|---|---|---|
| 01 | [Story & script](01_story_and_script.md) | What is the film *about*? How to structure it, write narration for speech/TTS, handle certainty, localise (Telugu code-mix example) |
| 02 | [Timing & edit](02_timing_and_edit.md) | How the voice drives every cut; beat tables; shot length; rhythm; transitions with meaning; chapter breaks |
| 03 | [Picture](03_picture.md) | The visual decision ladder; camera motion; procedural scenes catalogue (maps, diagrams, comparisons); satellite dives; colour; finishing; titles; subtitles incl. Indic scripts |
| 04 | [Sound](04_sound.md) | Four sound layers; music brief and composition method; SFX cue-sheet method; transitions; mix, ducking, loudness; with *and* without code |
| 05 | [Assets & licensing](05_assets_and_licensing.md) | Where to find footage/imagery/music legitimately; how to evaluate; how to look at candidates; honesty about stock |
| 06 | [Production & QA](06_production_and_qa.md) | Project phases and gates, resumable rendering, review passes, automated checks, how to work with the user, delivery note |
| 07 | [Templates](07_templates.md) | Fill-in templates: brief, identity line, beat table, shot list line, music brief, cue sheet, QA report, decision log, delivery note |
| 08 | [Worked example](08_worked_example_lakshadweep.md) | Act-by-act decision log of this film: line → thinking → choice → sound |
| 09 | [Quality bar & pitfalls](09_quality_bar_and_pitfalls.md) | The 40 details that make it look expensive; every failure we hit and the fix; anti-sameness system |
| 10 | [Implementation reference](10_implementation_reference.md) | Map of this repo's Python/ffmpeg toolchain, if you want to reuse it |

## How to use it

**For a new film with an LLM:** give it this folder (or at least 01–07 and 09), your topic, language and constraints, and say:
*"Follow the handbook. Fill the templates in chapter 07 as you go and show them to me before producing. Never skip chapter 06's review passes."*

**For a human director/editor:** chapters 01–04 are the craft; 05–06 are logistics; 07 is your paperwork; 08 is a case study.

**Relationship to other files in this repo**
- `DIRECTORS_GUIDE.md` — the short version of the thinking.
- `PLAYBOOK.md`, `PROMPTS.md` — how *this* film was implemented with Python/ffmpeg (a worked implementation, not the rules).
- `render/`, `build/` — the working code.

## Non-negotiables (the short list; details in the chapters)
1. The narration sets the clock; cuts land on ideas.
2. The picture illustrates the *idea* — draw it when it can't be filmed.
3. Every shot moves a little; nothing is a held slide.
4. Honest sourcing; everything credited; legends are labelled as legends.
5. Sound is designed in layers; voice always wins; loudness is measured.
6. Restraint: calm over dramatic, few transitions, almost no text.
7. You look at what you made (contact sheets, silent pass, audio-only pass) before showing it.
8. Each film gets its own identity (palette, music world, pace, transitions, diagrams).
