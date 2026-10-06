import numpy as np
import film_core as FC
from film_core import cut, cutg, tag, GT, TOTAL
from shots import *
import scenes_misc as SM
import assets as AS
from engine import *
import fx as FX


def _vf(sub, ss, speed=1.0):
    """frame function for split screens"""
    cache = {}

    def fn(t, d, st):
        if 'vs' not in cache:
            path = AS.conform(AS.video(sub), ss, d + 0.5, speed)
            cache['vs'] = VideoShot(path, d)
        return cache['vs'].frame(t)
    return fn


def split(dur, sa, sb, ssa=0.5, ssb=0.5, slider=((0, 0.18), (0.6, 0.78), (1, 0.5)), angle=7):
    return SM.split_wipe(dur, _vf(sa, ssa), _vf(sb, ssb), slider, angle)


def outro_overlay(img, T):
    t0 = FC.GT(8, 67.5)
    if T < t0:
        return img
    a = smooth((T - t0 - 0.6) / 1.2) * smooth((TOTAL - 0.8 - T) / 1.5)
    img = draw_title(img, 'L A K S H A D W E E P', 470, a, size=46, spacing=16, fname='Marcellus-Regular.ttf', color=(235, 242, 248), glow=True)
    img = draw_title(img, 'NASA GIBS  ·  Mixkit  ·  Wikimedia Commons  ·  Flickr contributors  ·  original score', 600, a * 0.7, size=22, spacing=3, fname='Jost[wght].ttf', color=(190, 205, 215), glow=False)
    img = draw_title(img, 'full credits in CREDITS.md', 650, a * 0.55, size=20, spacing=3, fname='Jost[wght].ttf', color=(170, 188, 200), glow=False)
    return img


def build():
    A = 8
    FC.OVERLAYS.append(outro_overlay)
    cut(A, 0.0, img('fl:21', 1.0, 1.25, (0.5, 0.5), (0.5, 0.5), fx=[fade_in(1.0), dust(0.15, 81, 30)]), 'dissolve', 0.01, 'teal', 'approach')
    cut(A, 4.9, vid('mk:1573', ss=2.0, zoom=(1.0, 1.08)), 'dissolve', 1.0, 'teal', 'fragile_beauty')
    cut(A, 9.25, vid('mk:1574', ss=3.0, zoom=(1.0, 1.14)), 'dissolve', 1.0, 'teal', 'tiny_island')
    cut(A, 13.55, lambda dur: split(dur, 'mk:26166', 'mk:44872', 3.0, 1.0, ((0, 0.12), (0.5, 0.55), (1, 0.5))), 'dissolve', 0.8, 'teal', 'tourism_split')
    cut(A, 16.8, img('fl:11', 1.0, 1.10, (0.5, 0.55), (0.5, 0.5), shake=0.3), 'dissolve', 0.7, 'warm', 'jobs')
    cut(A, 18.95, vid('mk:46200', ss=1.0, zoom=(1.0, 1.08)), 'dissolve', 0.8, 'warm', 'tourists')
    cut(A, 22.8, vid('mk:44872', ss=4.0, zoom=(1.0, 1.1), fx=[SM.bleach_fx(0.1, 0.9)]), 'dissolve', 0.9, 'bleach', 'pressure')
    cut(A, 26.25, lambda dur: split(dur, 'mk:2890', 'mk:12816', 1.0, 0.5, ((0, 0.5), (0.45, 0.22), (0.9, 0.78), (1, 0.5)), 5), 'dissolve', 0.9, 'teal', 'dev_vs_cons')
    cut(A, 31.1, vid('mk:44373', ss=3.0, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'dusk', 'not_one_or_other')
    cut(A, 34.1, vid('mk:1566', ss=2.0, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'dusk', 'balance')
    # back to the beginning: coral macro, pull back to the atoll
    cut(A, 37.65, vid('mk:100809', ss=4.0, zoom=(1.0, 1.1), fx=[dust(0.5, 82, 80, (210, 245, 255))]), 'dissolve', 0.8, 'teal', 'polyp_again')
    cut(A, 39.4, vid('mk:100835', ss=4.0, zoom=(1.0, 1.1), fx=[dust(0.5, 83, 80, (210, 245, 255))]), 'dissolve', 0.8, 'teal', 'polyp_again2')
    cut(A, 42.3, lambda dur: SM.island_to_earth(dur, 'bangaram'), 'dissolve', 1.4, 'teal', 'pull_back')
    # people take only what they need, live with the sea
    cut(A, 46.0, vid('mk:14341', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'dusk', 'fishermen_dusk')
    cut(A, 50.88, vid('mk:26972', ss=2.0, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'dusk', 'lesson')
    cut(A, 53.75, lambda dur: SM.island_to_earth(dur, 'agatti'), 'dissolve', 1.0, 'teal', 'island_to_earth')
    cut(A, 59.8, vid('mk:46148', ss=0.5, zoom=(1.0, 1.1)), 'dissolve', 1.6, 'cold', 'earth_india_end')
    cut(A, 62.6, vid('mk:44373', ss=6.0, zoom=(1.0, 1.1)), 'dissolve', 1.4, 'dusk', 'share_sunset')
    cut(A, 66.0, vid('mk:1080', ss=5.0, zoom=(1.0, 1.05), fx=[fade_out(2.5)]), 'dissolve', 1.2, 'dusk', 'end_sea')
    cutg(GT(8, 67.5) + 2.0, solid((0, 0, 0)), 'dip', 2.0, 'neutral', 'outro_black')
