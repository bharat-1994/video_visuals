import numpy as np
import film_core as FC
from film_core import cut, cutg, tag, GT
from shots import *
import scenes_a1 as S1
import scenes_misc as SM
from engine import smooth, draw_title
import fx as FX


def _title_overlay(img, T):
    """pre-roll title: Telugu name + spaced Latin name + hairline"""
    t0, t1 = 1.0, 4.7
    if not (t0 <= T <= t1 + 0.4):
        return img
    a = smooth((T - t0) / 1.2) * smooth((t1 + 0.4 - T) / 0.7)
    drift = int(-14 * (T - t0))
    img = draw_title(img, 'లక్షద్వీప్', 470, a, size=190, spacing=0, fname='Ramaraja-Regular.ttf', color=(255, 255, 255), dx=drift)
    img = draw_title(img, 'L A K S H A D W E E P', 640, a * 0.9, size=40, spacing=14, fname='Marcellus-Regular.ttf', color=(225, 236, 245), glow=False, dx=drift)
    return img


def build():
    FC.OVERLAYS.append(_title_overlay)
    # ---- pre-roll: black -> dark swell + title -> remote island on the first word
    cutg(0.0, vid('mk:1164', ss=2.0, speed=0.6, zoom=(1.0, 1.10), fx=[fade_in(2.0), dust(0.2, 11, 60)]), 'cut', 0, 'storm', 'preroll')
    cutg(GT(1, 0.0) - 0.05, vid('mk:1575', ss=1.0, zoom=(1.0, 1.12), pan=(0, 0, 0.03, -0.02), fx=[dust(0.15, 4, 50)]), 'flare', 0.7, 'teal', 'aerial0')
    cut(1, 2.3, lambda dur: S1.intro_map(dur, 2.3), 'dissolve', 1.2, 'teal', 'map_dive')
    cut(1, 18.5, lambda dur: S1.hyderabad(dur, 18.5), 'iris', 0.7, 'warm', 'hyderabad')
    cut(1, 22.1, lambda dur: S1.eez(dur, 22.1), 'dissolve', 0.9, 'teal', 'eez')
    # land is little, the sea is vast
    cut(1, 27.1, vid('mk:1574', ss=0.5, zoom=(1.0, 1.15), fx=[dust(0.12, 6, 35)]), 'dissolve', 1.1, 'teal', 'sea_vast')
    # not about the land... but the sea
    cut(1, 30.2, vid('mk:4466', ss=1.0, zoom=(1.0, 1.08), fx=[rays(0.18)]), 'dissolve', 1.2, 'teal', 'sky_from_below')
    # three questions
    cut(1, 34.3, vid('mk:44373', ss=1.0, zoom=(1.0, 1.10), fx=[dust(0.1, 3, 30)]), 'dissolve', 1.0, 'dusk', 'q_intro')
    cut(1, 37.65, vid('mk:100809', ss=2.0, zoom=(1.0, 1.1), fx=[dust(0.4, 2, 70, (210, 240, 255))]), 'whip', 0.45, 'teal', 'q1')
    cut(1, 39.40, img('fl:11', 1.0, 1.10, (0.5, 0.55), (0.45, 0.5), shake=0.5, fx=[dust(0.2, 7, 40)]), 'whip', 0.45, 'warm', 'q2')
    cut(1, 42.72, lambda dur: SM.cyclone(dur, zoom=(1.0, 1.5), swirl=1.0), 'whip', 0.45, 'storm', 'q3')
    cut(1, 45.0, solid((0, 0, 0)), 'dip', 1.2, 'neutral', 'fadeout')
    tag(1, 12.4, 17.4, 'Agatti Atoll', '10.86°N  72.18°E')
