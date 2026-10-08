"""One import that loads the shared library into the scene_v2 registries (BG, ASSETS, CAST, CUSTOM, AMBIENCE, FX):
all backgrounds, props, cast and custom shots built so far (currently the Vietnam stack). New episodes: `import library.register`
and then ADD new things in episodes/<slug>/assets_<slug>.py via setup(). Anything reusable gets promoted into library/ later
(with a catalog picture) so the next episode can reuse it.  Browse: library/catalog/CATALOG.md and the sheets beside it."""
import sys, os
K = os.getcwd(); sys.path.insert(0, K); sys.path.insert(0, os.path.join(K, "engine"))
from episodes.vietnam import film_setup                       # noqa: seeds engine/scene.py registries
import scene, scene_v2
for _d in ("BG", "ASSETS", "CAST", "CUSTOM", "AMBIENCE"): getattr(scene_v2, _d).update(getattr(scene, _d))
from episodes.vietnam.v2 import setup_v2                      # noqa: v2 registries + overrides
from episodes.vietnam.key import SHOT_FNS as VIETNAM_KEY_SHOTS  # hand-coded Vietnam shots (not reusable as is)
