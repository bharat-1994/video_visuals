import numpy as np
import film_core as FC
from film_core import cut, cutg, tag, GT
from shots import *
import scenes_misc as SM
import assets as AS
from engine import *
import fx as FX


def flash(f, t, d):
    """lightning flashes"""
    import math
    k = math.sin(t * 7.3) * math.sin(t * 3.1 + 1.0)
    if k > 0.93:
        return np.clip(f.astype(np.float32) + 90 * (k - 0.93) / 0.07, 0, 255).astype(np.uint8)
    return f


def build():
    A = 7
    cut(A, 0.0, vid('mk:1577', ss=3.0, zoom=(1.0, 1.1), fx=[fade_in(0.8)]), 'dissolve', 0.01, 'teal', 'beautiful')
    cut(A, 3.84, solid((0, 0, 0)), 'cut', 0, 'neutral', 'no_black')
    cut(A, 4.5, vid('mk:46148', ss=1.0, zoom=(1.0, 1.15)), 'dissolve', 0.9, 'cold', 'earth_india')
    cut(A, 9.66, lambda dur: SM.sea_level(dur), 'dissolve', 1.0, 'teal', 'sea_level')
    # coral bleaching 2016
    cut(A, 22.1, vid('mk:44868', ss=1.0, zoom=(1.0, 1.08)), 'dissolve', 0.9, 'teal', 'reef_healthy')
    cut(A, 24.15, vid('mk:44872', ss=1.0, zoom=(1.0, 1.1), fx=[SM.bleach_fx(0.05, 0.95)]), 'dissolve', 0.8, 'teal', 'reef_bleaching')
    cut(A, 29.15, lambda dur: SM.heat_map(dur), 'dissolve', 1.0, 'teal', 'elnino_heat')
    cut(A, 34.25, vid('mk:44871', ss=1.0, zoom=(1.0, 1.1), fx=[SM.bleach_fx(0.0, 0.3)]), 'dissolve', 0.9, 'bleach', 'dead_reef')
    cut(A, 36.4, vid('mk:51506', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.7, 'storm', 'waves_on_shore')
    # Ockhi 2017
    cut(A, 38.4, lambda dur: SM.cyclone(dur, zoom=(1.0, 1.6), swirl=1.4), 'dissolve', 0.5, 'storm', 'ockhi_vi')
    cut(A, 41.0, vid('mk:48855', ss=1.0, zoom=(1.0, 1.1), fx=[flash]), 'dissolve', 0.5, 'storm', 'storm_front')
    cut(A, 43.1, vid('mk:45239', ss=1.0, zoom=(1.0, 1.1), fx=[flash]), 'dissolve', 0.6, 'storm', 'lighthouse_waves')
    cut(A, 45.5, vid('mk:17969', ss=1.0, zoom=(1.0, 1.08)), 'dissolve', 0.9, 'storm', 'gulls_storm')
    # connectivity
    cut(A, 47.95, vid('mk:22632', ss=2.0, zoom=(1.0, 1.1)), 'dissolve', 1.0, 'teal', 'plane_leaving')
    cut(A, 49.75, lambda dur: SM.route_map(dur,
        [(0, 74.6, 10.2, 8.0), (dur, 74.2, 10.4, 6.0)],
        routes=[dict(pts=[(76.27, 9.97), (75.0, 10.3), (73.5, 10.6), (72.18, 10.86)], t0=0.1, t1=1.8, color=(255, 214, 120), width=4)],
        markers=[(76.27, 9.97, 0.0, (255, 225, 150), 10, True), (72.18, 10.86, 1.6, (130, 235, 255), 10, True)],
        labels=[('KOCHI', 76.27, 9.97, 0.2, 2.2, -120, 26), ('AGATTI', 72.18, 10.86, 1.6, 2.2, 22, -22)], extra=('mid_north',)), 'dissolve', 0.7, 'teal', 'kochi_agatti')
    cut(A, 51.5, vid('mk:27994', ss=18.0, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'teal', 'plane_landing')
    cut(A, 54.5, vid('mk:34290', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.9, 'teal', 'cargo_ship')
    # internet: satellite
    cut(A, 57.9, vid('mk:45033', ss=2.0, zoom=(1.0, 1.12)), 'dissolve', 1.0, 'cold', 'satellite_night')
    cut(A, 62.2, lambda dur: SM.cable_map(dur), 'dissolve', 1.0, 'teal', 'cable')
    # fresh water
    cut(A, 67.5, vid('mk:1280', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'cold', 'drop')
    cut(A, 69.2, vid('mk:1080', ss=3.0, zoom=(1.0, 1.08)), 'dissolve', 0.9, 'cold', 'sea_around')
    cut(A, 72.05, vid('mk:100914', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.9, 'teal', 'pour')
    cut(A, 74.7, vid('mk:2208', ss=2.0, zoom=(1.0, 1.1)), 'dissolve', 0.9, 'teal', 'ripples')
    cut(A, 76.8, vid('mk:1577', ss=8.0, zoom=(1.0, 1.1), fx=[fade_out(1.5)]), 'dissolve', 1.2, 'warm', 'hope')
    tag(A, 49.9, 52.5, 'Agatti Airport', '10.82°N  72.18°E')
