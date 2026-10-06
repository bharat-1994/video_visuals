import numpy as np
import film_core as FC
from film_core import cut, cutg, tag, GT
from shots import *
import scenes_misc as SM
import scenes_a1 as S1
import assets as AS
import geo as G
from engine import *
import fx as FX

KARACHI = (66.99, 24.86); KOCHI = (76.27, 9.97); LAK = (72.64, 10.57)


def flag_beach(dur, bg_sub='fl:25', hoist=(0.0, 1.0), wind=1.0, t_hoist=(0.0, 3.0), zoom=(1.0, 1.08)):
    path = AS.still(bg_sub)
    st = StillShot(path, dur, zoom[0], zoom[1], (0.5, 0.5), (0.5, 0.5))

    def fn(t, d, s):
        st.dur = d
        f = st.frame(t)
        h = lerp(hoist[0], hoist[1], smooth((t - t_hoist[0]) / max(t_hoist[1] - t_hoist[0], 1e-3)))
        f = SM.flag_overlay(f, t * 1.0 + 3.0, 880, 300 + int(180 * (1 - h)) - 40, width=760, hoist=1.0, wind=wind)
        f = FX.light_leak(f, t, 0.0, d, (255, 190, 120), 0.25, 'right')
        return f
    return FuncShotF(fn, dur)


def sky_flag(dur, hoist=(0.0, 1.0), t_h=(0.3, 3.0)):
    p = AS.conform(AS.video('mk:2893'), 0.0, dur + 1.0)
    vs = VideoShot(p, dur)

    def fn(t, d, s):
        f = vs.frame(t)
        h = lerp(hoist[0], hoist[1], smooth((t - t_h[0]) / (t_h[1] - t_h[0])))
        f = SM.flag_overlay(f, t * 1.0, 760, 140 + int(560 * (1 - h)), width=980, hoist=1.0, wind=1.1)
        return f
    return FuncShotF(fn, dur)


def build():
    A = 5
    # 1947: independence
    cut(A, 0.0, lambda dur: sky_flag(dur, (0.0, 1.0), (0.4, 2.6)), 'dissolve', 0.01, 'warm', 'flag_sky')
    cut(A, 2.15, lambda dur: SM.year_card(dur, '1947', 'INDEPENDENCE', bg=None, t_in=0.2), 'dissolve', 0.8, 'neutral', 'year1947')
    # but there was a problem
    cut(A, 5.6, lambda dur: SM.route_map(dur,
        [(0, 77.0, 22.0, 62.0), (dur, 76.0, 18.0, 52.0)],
        markers=[(72.64, 10.57, 1.5, (130, 235, 255), 8, True)],
        labels=[('LAKSHADWEEP', 72.64, 10.57, 2.2, 6.0, 20, 30)], dim=0.0), 'dissolve', 0.9, 'sepia', 'far_corner')
    cut(A, 12.8, lambda dur: SM.route_map(dur,
        [(0, 68.0, 14.0, 22.0), (dur, 70.0, 12.0, 16.0)],
        routes=[dict(pts=[(50.0, 26.0), (60.0, 20.0), (72.0, 11.0), (86.0, 5.0), (96.0, 4.0)], t0=0.2, t1=3.2, color=(255, 214, 120), width=4),
                dict(pts=[(45.0, 12.0), (60.0, 11.0), (71.0, 10.4), (77.0, 7.0), (92.0, 5.5)], t0=0.6, t1=3.4, color=(255, 214, 120), width=4)],
        markers=[(72.64, 10.57, 1.0, (130, 235, 255), 10, True)]), 'dissolve', 0.9, 'teal', 'sea_routes')
    cut(A, 16.3, vid('mk:5016', ss=2.0, speed=0.8, zoom=(1.0, 1.06), fx=[dust(0.1, 51, 30)]), 'dissolve', 0.9, 'sepia', 'story_waves')
    # the chase
    cut(A, 19.2, lambda dur: SM.route_map(dur,
        [(0, 71.5, 17.0, 20.0), (dur, 72.3, 12.0, 11.0)],
        routes=[dict(pts=[KARACHI, (68.5, 20.0), (70.5, 15.5), (72.2, 12.0), (72.6, 10.7)], t0=1.0, t1=6.8, color=(255, 100, 90), width=4),
                dict(pts=[KOCHI, (75.2, 10.2), (73.8, 10.5), (72.64, 10.57)], t0=0.6, t1=5.6, color=(120, 235, 255), width=4)],
        markers=[(KARACHI[0], KARACHI[1], 0.3, (255, 120, 110), 8, True), (KOCHI[0], KOCHI[1], 0.3, (130, 235, 255), 8, True), (72.64, 10.57, 5.6, (255, 255, 255), 12, True)],
        labels=[]), 'dissolve', 0.9, 'teal', 'chase')
    # flag raised
    cut(A, 26.3, lambda dur: flag_beach(dur, 'fl:25', (0.0, 1.0), 1.0, (0.2, 2.4)), 'dissolve', 0.5, 'warm', 'flag_hoist')
    # a few hours later the other ship reached
    cut(A, 29.2, lambda dur: SM.route_map(dur,
        [(0, 72.4, 11.2, 9.0), (dur, 72.6, 10.8, 4.2)],
        routes=[dict(pts=[(70.5, 15.5), (72.0, 12.2), (72.6, 10.7)], t0=0.1, t1=3.0, color=(255, 100, 90), width=4)],
        markers=[(72.64, 10.57, 0.0, (255, 255, 255), 12, True)], dim=0.05), 'dissolve', 0.6, 'teal', 'late_ship')
    # but the flag was already flying
    cut(A, 33.3, lambda dur: flag_beach(dur, 'fl:25', (1.0, 1.0), 1.15, (0.0, 0.1), (1.0, 1.1)), 'dissolve', 0.5, 'warm', 'flag_flying')
    cut(A, 35.7, vid('mk:7387', ss=3.0, zoom=(1.0, 1.08)), 'dissolve', 1.0, 'warm', 'boat_island')
    # became part of India
    cut(A, 37.7, lambda dur: SM.route_map(dur,
        [(0, 75.0, 14.0, 22.0), (dur, 77.0, 18.0, 36.0)],
        routes=[dict(pts=[(72.64, 10.57), (74.5, 11.5), (76.3, 11.9)], t0=0.2, t1=1.8, color=(255, 175, 80), width=5, dash=False, head=False)],
        markers=[(72.64, 10.57, 0.0, (255, 255, 255), 12, True)], dim=0.0), 'dissolve', 0.9, 'warm', 'part_of_india')
    # 1956: UT
    cut(A, 39.7, lambda dur: SM.year_card(dur, '1956', 'UNION TERRITORY', bg=None, t_in=0.3), 'dissolve', 0.9, 'neutral', 'year1956')
    # 3 groups: Laccadive, Minicoy, Amindivi
    cut(A, 44.7, lambda dur: SM.route_map(dur,
        [(0, 73.0, 10.2, 7.0), (dur, 73.0, 10.2, 6.2)],
        markers=[(72.4, 10.7, 0.6, (130, 235, 255), 18, True), (73.04, 8.28, 1.8, (255, 225, 150), 14, True), (72.8, 11.4, 3.0, (255, 160, 140), 16, True)],
        labels=[('LACCADIVE', 72.4, 10.7, 0.8, 4.5, 26, 8), ('MINICOY', 73.04, 8.28, 2.0, 4.5, 26, 8), ('AMINDIVI', 72.8, 11.4, 3.2, 4.5, 26, -26)], extra=('mid_north',)), 'dissolve', 0.9, 'teal', 'three_groups')
    # 1973: Lakshadweep
    cut(A, 49.3, lambda dur: SM.year_card(dur, '1973', 'LAKSHADWEEP', bg=None, t_in=0.3), 'dissolve', 0.9, 'neutral', 'year1973')
    # a lakh of islands... in reality 36
    cut(A, 54.2, lambda dur: S1.intro_map_lakh(dur, 54.2), 'dissolve', 1.0, 'teal', 'lakh_again')
