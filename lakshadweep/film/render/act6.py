import film_core as FC
from film_core import cut, cutg, tag, GT
from shots import *
import scenes_misc as SM
import assets as AS
from engine import *
import fx as FX


def build():
    A = 6
    cut(A, 0.0, img('fl:11', 1.0, 1.10, (0.5, 0.55), (0.45, 0.5), shake=0.4, fx=[fade_in(0.8), dust(0.2, 61, 40)]), 'dissolve', 0.01, 'warm', 'village_boats')
    cut(A, 3.36, img('fl:13', 1.0, 1.10, (0.5, 0.5), (0.5, 0.45), shake=0.3), 'dissolve', 0.9, 'warm', 'kids_talk')
    # Minicoy & Mahl
    cut(A, 7.0, lambda dur: SM.route_map(dur,
        [(0, 73.0, 9.4, 6.0), (dur, 73.04, 8.28, 0.55)],
        markers=[(73.04, 8.28, 1.0, (255, 225, 150), 10, True)], labels=[('MINICOY', 73.04, 8.28, 1.2, 3.6, 24, -24)], extra=('mid_minicoy', 'minicoy'), dim=0.0), 'dissolve', 0.9, 'teal', 'minicoy')
    cut(A, 10.6, lambda dur: SM.route_map(dur,
        [(0, 73.2, 6.6, 9.0), (dur, 73.3, 5.6, 12.0)],
        routes=[dict(pts=[(73.04, 8.28), (73.3, 6.8), (73.5, 4.2)], t0=0.3, t1=2.8, color=(130, 235, 255), width=4)],
        markers=[(73.04, 8.28, 0.0, (255, 225, 150), 10, True), (73.5, 4.2, 2.6, (255, 225, 150), 10, True)],
        labels=[('MALDIVES', 73.5, 4.2, 2.6, 3.6, 26, 6)]), 'dissolve', 0.9, 'teal', 'maldives_link')
    cut(A, 14.22, img('fl:23', 1.0, 1.12, (0.5, 0.55), (0.5, 0.5), shake=0.3, fx=[dust(0.15, 62, 30)]), 'dissolve', 0.9, 'warm', 'tradition')
    # matrilineal
    cut(A, 16.9, lambda dur: SM.matri(dur), 'dissolve', 1.0, 'neutral', 'matrilineal')
    # livelihood: tuna
    cut(A, 27.15, vid('mk:4291', ss=0.5, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'teal', 'tuna_school')
    cut(A, 31.7, vid('mk:47138', ss=0.5, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'warm', 'pole_line')
    cut(A, 35.45, vid('mk:47317', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.7, 'warm', 'casting')
    cut(A, 39.1, vid('mk:49186', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'teal', 'aerial_fisher')
    cut(A, 42.55, vid('mk:44976', ss=0.5, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'teal', 'school_alive')
    # food
    cut(A, 46.5, img('fl:7', 1.0, 1.12, (0.5, 0.5), (0.5, 0.5)), 'whip', 0.35, 'warm', 'snapper')
    cut(A, 47.95, vid('mk:22886', ss=0.5, zoom=(1.0, 1.08)), 'dissolve', 0.5, 'warm', 'grill')
    cut(A, 49.9, img('fl:2', 1.0, 1.14, (0.5, 0.5), (0.5, 0.5)), 'dissolve', 0.6, 'warm', 'fish_sand')
    cut(A, 52.2, vid('mk:31955', ss=0.5, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'warm', 'fish_market')
    # dances (rhythm of water until real dance footage is available)
    cut(A, 55.2, vid('mk:20418', ss=2.0, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'dusk', 'rhythm_boats')
    cut(A, 58.0, vid('mk:18758', ss=1.0, zoom=(1.0, 1.08)), 'dissolve', 1.0, 'dusk', 'canoe_sunset')
    cut(A, 61.55, vid('mk:14341', ss=1.0, zoom=(1.0, 1.1), fx=[fade_out(1.6)]), 'dissolve', 0.9, 'dusk', 'work_songs')
