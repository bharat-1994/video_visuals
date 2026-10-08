"""shots.json -> DIRECTION.md (humans) and batch slices (builders).
   python3 engine/spec2md.py episodes/<slug>            -> writes DIRECTION.md
   python3 engine/spec2md.py episodes/<slug> qwen B01   -> also writes BATCH_B01.md with only that builder's shots
shots.json is the single source of truth; never hand-edit the generated markdown."""
import sys, json, os
d = sys.argv[1]; J = json.load(open(os.path.join(d, "shots.json"))); E, S = J["episode"], J["shots"]

def shot_md(s):
    m = int(s["start"]//60); e = s["start"]+s["dur"]
    L = [f"### {s['id']} · {m}:{s['start']%60:05.2f}–{int(e//60)}:{e%60:05.2f} ({s['dur']:.2f} s) · builder: {s['builder']}",
         f"**Narration:** \"{s['narration']}\"  ", f"**Word times (s from shot start):** " + ", ".join(f"{k} {v:.2f}" for k, v in s["words"].items()) + "  ",
         f"**Visual:** {s['visual']}  ", f"**Staging:** {s['staging']}  ", f"**Camera:** {s['camera']}  "]
    if s["text"]: L.append("**Text:** " + "; ".join(f"{x['kind']} \"{x['text']}\" @ {x['t']:.2f}" for x in s["text"]) + "  ")
    L.append("**SFX (auto-mixed from shots.json; time your pops to match):** " + ", ".join(f"{n} {t:.2f} ({g} dB)" for n, t, g in s["sfx"]) + "  ")
    L.append("**Assets:** " + ", ".join(s["assets"]) + "  ")
    if s["builder"] != "director": L += ["**CHECKS:**"] + [f"- [ ] {c}" for c in s["checks"]]
    return "\n".join(L)

head = [f"# {E['title']}", f"*{E['act']}*", "", f"- **Narration:** {E['narration']}", f"- **Assets module:** {E['assets_module']}",
        f"- **Assembly:** {E['assembly']}", f"- **Key shots (director):** {', '.join(E['key_shots'])}", "", "## Cast", "| id | look | call |", "|---|---|---|"]
head += [f"| {a} | {b} | `{c}` |" for a, b, c in E["cast"]]
head += ["", "## Assets (signature features)", "| asset | signature features | shots |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in E["assets"]]
head += ["", "## Palettes"] + [f"- **{k}:** {', '.join(v)}" for k, v in E["palettes"].items()] + ["", "## Motifs", E["motifs"], "", "## Shots"]
open(os.path.join(d, "DIRECTION.md"), "w").write("\n".join(head) + "\n\n" + "\n\n".join(shot_md(s) for s in S) + "\n")
if len(sys.argv) > 3:
    who, b = sys.argv[2], sys.argv[3]; mine = [s for s in S if s["builder"] == who]
    open(os.path.join(d, f"BATCH_{b}.md"), "w").write(f"# Batch {b}: {who} builds {', '.join(s['id'] for s in mine)}\n\n" + "\n\n".join(shot_md(s) for s in mine) + "\n")
print("ok")
