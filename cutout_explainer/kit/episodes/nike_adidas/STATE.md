# Nike vs Adidas ("The Sneaker War"): state
Status: audio received, plan written, task cards made (22). Not yet built. Nothing committed to main.
Model roles this episode: director = Sonnet 5.5 (plan, key shots, cast, judging), builders = Haiku 5.5 high (props, shot lines), Opus medium only for an item Haiku fails twice.
Token log: director so far about 100k (reading project docs, 8 catalog sheets, writing plan).

## Done
- `narration.wav` (339.96 s, five parts joined with 0.3 s gaps), `words.json` (755 words, from the user's Whisper transcript, offsets applied), `segs.json` (97 shots, hand-cut at clauses), `END.txt`.
- `PLAN.md`: chapters, motifs, bg budget (every bg <= 7 shots), 12 key shots, sound, motion list, people list, 97-line shot table, 22 new assets.
- `TASKS/*.md`: 22 cards (`tools/make_cards.py`). Pack: `builder/PACK.md` (about 780 tokens); `python3 tools/make_pack.py --lines` for shot-line builders.

## Open items / hand-offs (in order)
1. User checks Act I audio for "Audie" vs "Adi" (S28, about 99.5 s) and approves the plan.
2. Builder batches, one fresh Haiku session each, pack + its cards + this file:
   - B1 (core shoes): sneaker_lowtop, sneaker_hightop, sneaker_terrace, sneaker_runner_stack, sneaker_runner_pods
   - B2: football_boot, shoe_box, box_pile, shoe_shelf, videotape
   - B3: cash_register, cash_cow, engine_block, balance_scale, basketball
   - B4: shop_app, billboard, chained_bag, sale_badge, empty_lot
   - B5: cobbler_bench, ribbon_sign
   - B6: new backgrounds bg_herzogenaurach, bg_oregon, bg_track_field (cards to add; they are full-frame, so they need their own cards with size 1280x720)
3. Director: cast rigs jordan, adi, rudi, knight, bowerman, celebrity (`assets.py`); key shots in `key.py`.
4. Shot-line builders: 85 lines in batches of about 25, then `engine/audit.py`, `engine/layout_check.py`, `bakeoff/score.py`, then a 720p sheet, look, fix, final 1080p.
5. Fact notes for the script: "Jordan wore their shoes in high school" and "$6.6 billion annual" are the script's claims, drawn as written; Nike's brand-name wordmarks are plain lettering only.
