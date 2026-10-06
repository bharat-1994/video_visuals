import numpy as np
import film_core as FC
from film_core import cut, cutg, tag, GT
from shots import *
import scenes_a2 as S2
import scenes_misc as SM
from engine import smooth
import fx as FX


XS1 = [(0, 960, 640, 1.0), (7.0, 960, 600, 1.0), (8.0, 960, 560, 1.15)]
XS2 = [(0, 960, 520, 1.1), (4.2, 960, 400, 2.2)]
XS3 = [(0, 960, 330, 2.2), (3.0, 960, 560, 1.0), (5.6, 960, 600, 0.95), (9.0, 960, 420, 1.15), (12.3, 960, 330, 1.4)]


def build():
    A = 2
    cut(A, 0.0, vid('mk:4466', ss=4.0, zoom=(1.0, 1.06), fx=[fade_in(1.0), rays(0.16)]), 'dissolve', 0.01, 'teal', 'open')
    cut(A, 1.4, img('fl:4', 1.0, 1.12, (0.5, 0.55), (0.55, 0.5), shake=0.4, fx=[dust(0.2, 8, 40)]), 'dissolve', 0.9, 'warm', 'flat_beach')
    cut(A, 5.94, img('fl:6', 1.05, 1.22, (0.5, 0.45), (0.5, 0.5), fx=[dust(0.2, 9, 40)]), 'whip', 0.4, 'warm', 'coral_in_hand')
    cut(A, 8.08, lambda dur: S2.cross_section(dur, 8.08, XS1, show_coral=False), 'dissolve', 1.2, 'teal', 'xs1_rise')
    cut(A, 16.12, lambda dur: SM.ridge_fly(dur, 16.12), 'dissolve', 0.9, 'teal', 'ridge')
    cut(A, 19.16, lambda dur: S2.cross_section(dur, 19.16, XS2, show_coral=False), 'dissolve', 0.9, 'teal', 'xs2_summit')
    # polyps
    cut(A, 23.4, vid('mk:100809', ss=1.0, zoom=(1.0, 1.12), fx=[dust(0.5, 13, 80, (210, 245, 255))]), 'dissolve', 0.8, 'teal', 'polyp1')
    cut(A, 26.0, vid('mk:100835', ss=1.0, zoom=(1.0, 1.1), fx=[dust(0.5, 14, 80, (210, 245, 255))]), 'dissolve', 0.6, 'teal', 'polyp2')
    cut(A, 28.6, vid('mk:100811', ss=1.0, zoom=(1.0, 1.12), fx=[dust(0.5, 15, 80, (210, 245, 255))]), 'dissolve', 0.6, 'teal', 'polyp3')
    cut(A, 31.0, lambda dur: S2.cross_section(dur, 31.0, XS3, grow=(31.0, 38.0), sink=(36.6, 43.2)), 'dissolve', 1.0, 'teal', 'xs3_growth')
    cut(A, 43.3, lambda dur: S2.atoll_ring(dur, 43.3, morph=(2.4, 5.0)), 'dissolve', 1.2, 'teal', 'ring_to_real')
    cut(A, 51.36, vid('mk:100821', ss=1.0, zoom=(1.0, 1.1), fx=[dust(0.35, 16, 60, (255, 240, 220))]), 'dissolve', 0.9, 'warm', 'polyp_rings')
    cut(A, 53.9, img('fl:25', 1.0, 1.10, (0.5, 0.5), (0.45, 0.55), shake=0.4, fx=[dust(0.2, 17, 40)]), 'dissolve', 0.9, 'warm', 'beach_steps')
    cut(A, 56.6, vid('mk:5016', ss=1.0, speed=0.75, zoom=(1.0, 1.08), fx=[fade_out(2.0)]), 'dissolve', 0.9, 'warm', 'white_sand')
    tag(A, 49.0, 52.0, 'Atoll', 'Bangaram, Lakshadweep')
