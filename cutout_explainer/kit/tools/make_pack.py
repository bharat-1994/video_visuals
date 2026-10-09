"""Build the fixed builder pack (identical for every builder session, so it caches): builder/PACK.md
   python3 tools/make_pack.py [--lines]      --lines adds the scene grammar + catalog list (for shot-line builders)
Prints the size in estimated tokens (chars/4); keep it under ~15k so a whole session stays far below 100k per request."""
import sys, os
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parts = ["bakeoff/RULES.md", "bakeoff/LIB_CHEATSHEET.md"] + (["engine/SCENE_LANGUAGE.md"] if "--lines" in sys.argv else [])
out = "\n\n---\n\n".join(f"<!-- {p} -->\n" + open(os.path.join(K, p)).read() for p in parts)
if "--lines" in sys.argv:
    cat = open(os.path.join(K, "library/catalog/CATALOG.md")).read()
    out += "\n\n---\n\n<!-- library/catalog/CATALOG.md (names you may use) -->\n" + "\n".join(l.split("|")[1].strip() + " " + l.split("|")[2].strip() + " " + l.split("|")[3].strip() for l in cat.splitlines() if l.startswith("| asset") or l.startswith("| bg") or l.startswith("| cast"))
os.makedirs(os.path.join(K, "builder"), exist_ok=True)
fn = os.path.join(K, "builder", "PACK_LINES.md" if "--lines" in sys.argv else "PACK.md"); open(fn, "w").write(out); print(fn, "~%d tokens" % (len(out)//4))
