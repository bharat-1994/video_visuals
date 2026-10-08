"""Beat-gap measurement: a 'beat' = something new the viewer sees, tied to a narration word.
Counts @word pop-ins, out@ exits, animated params, pose2 changes, talk start, counter ends, and @words inside fn/fx kv
(at=, pins, targets...). The cut itself is a beat at t=0. Returns the largest gap (s) in a shot."""
import re
def max_gap(sh):
    beats = [0.0, sh.dur]
    for e in sh.els:
        for x in (e["t_at"], e["t_out"]):
            if x is not None: beats.append(x)
        beats += [v[2] for v in e["anim_t"].values()]
        for k, v in e["kv"].items():
            for w in re.findall(r"@[^\s,'\"\]~:]+", str(v)):
                try: beats.append(sh.T(w))
                except Exception: pass
        if e["typ"] == "cnt" and e["t_at"] is not None: beats.append(e["t_at"] + e["kv"].get("dur", 1.2))
    end = min(sh.dur, (sh.words[-1][1] + 0.8) if sh.words else sh.dur)   # a pause after the last word may be held
    beats.append(end)
    b = sorted(x for x in beats if 0 <= x <= end)
    return max(y - x for x, y in zip(b, b[1:]))
