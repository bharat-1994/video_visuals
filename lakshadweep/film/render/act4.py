import film_core as FC
from film_core import cut, cutg, tag, GT
from shots import *
import scenes_misc as SM
import assets as AS
from engine import smooth, VideoShot
import fx as FX

KANNUR = (75.37, 11.87); AMINI = (72.73, 11.12); KAVARATTI = (72.64, 10.57); MADRAS = (80.27, 13.08)
LAK = (72.9, 10.6)


def _sunset_base(sub, ss):
    def make(dur):
        path = AS.conform(AS.video(sub), ss, dur)
        vs = VideoShot(path, dur)
        return vs
    return make


def portuguese(dur):
    vs = _sunset_base('mk:44373', 1.0)(dur)
    return SM.carracks(dur, lambda t, d, st: vs.frame(t), ships=((0.34, 0.472, 0.34), (0.62, 0.466, 0.22), (0.78, 0.47, 0.16)))


def build():
    A = 4
    # rulers of the Kannur region
    cut(A, 0.0, lambda dur: SM.route_map(dur,
        [(0, 74.2, 11.2, 7.0), (dur, 74.0, 11.2, 5.2)],
        routes=[dict(pts=[KANNUR, (74.4, 11.55), AMINI], t0=1.5, t1=4.5, color=(255, 214, 120), width=3),
                dict(pts=[KANNUR, (74.0, 11.2), (73.0, 10.9), KAVARATTI], t0=2.2, t1=5.4, color=(255, 214, 120), width=3)],
        markers=[(KANNUR[0], KANNUR[1], 0.3, (255, 225, 150), 16, True), (AMINI[0], AMINI[1], 4.5, (130, 235, 255), 8, True), (KAVARATTI[0], KAVARATTI[1], 5.4, (130, 235, 255), 8, True)],
        labels=[('KANNUR', KANNUR[0], KANNUR[1], 0.6, 5.8, 24, -16)], extra=('mid_north',), dim=0.05), 'dissolve', 0.01, 'sepia', 'kannur')
    cut(A, 6.1, img('fl:31', 1.0, 1.12, (0.5, 0.5), (0.5, 0.5), shake=0.3, fx=[dust(0.2, 41, 40)]), 'dissolve', 1.0, 'sepia', 'malabar_nets')
    cut(A, 11.1, lambda dur: SM.route_map(dur,
        [(0, 62.0, 13.5, 44.0), (dur, 64.0, 11.0, 40.0)],
        routes=[dict(pts=[(45.0, 12.8), (55.0, 14.0), (65.0, 12.6), (73.0, 11.4), (75.4, 11.5)], t0=0.2, t1=3.2, color=(255, 200, 120), width=3),
                dict(pts=[(58.6, 23.6), (66.0, 18.0), (72.0, 12.0), (75.4, 11.5)], t0=0.6, t1=3.6, color=(255, 200, 120), width=3),
                dict(pts=[(75.4, 11.5), (74.2, 8.5), (73.4, 4.2), (79.85, 6.93)], t0=2.0, t1=5.2, color=(130, 235, 255), width=3)],
        markers=[(45.0, 12.8, 0.1, (255, 225, 150), 8, False), (58.6, 23.6, 0.3, (255, 225, 150), 8, False), (75.4, 11.5, 2.4, (255, 225, 150), 10, True), (72.9, 10.6, 3.0, (130, 235, 255), 10, True),
                 (73.4, 4.2, 4.2, (130, 235, 255), 8, True), (79.85, 6.93, 5.0, (130, 235, 255), 8, True)],
        labels=[('THE ARABIAN SEA TRADE', 58.0, 8.5, 0.8, 5.0, 0, 0)]), 'dissolve', 1.0, 'sepia', 'trade_chain')
    # Portuguese arrive
    cut(A, 16.5, portuguese, 'dissolve', 1.0, 'dusk', 'carracks')
    # pepper trade: Lisbon -> Calicut
    cut(A, 20.2, lambda dur: SM.route_map(dur,
        [(0, 28.0, 8.0, 140.0), (dur, 60.0, 12.0, 85.0)],
        routes=[dict(pts=[(-9.14, 38.7), (-17.5, 28.0), (-17.0, 8.0), (-5.0, -20.0), (18.4, -34.4), (35.0, -26.0), (42.0, -4.0), (58.0, 4.0), (75.8, 11.25)], t0=0.1, t1=3.3, color=(255, 120, 100), width=4)],
        markers=[(-9.14, 38.7, 0.0, (255, 225, 150), 10, True), (75.8, 11.25, 3.2, (130, 235, 255), 10, True)],
        labels=[('LISBON', -9.14, 38.7, 0.3, 3.5, 24, -18), ('CALICUT', 75.8, 11.25, 3.2, 3.9, -150, -24)]), 'dissolve', 0.9, 'sepia', 'pepper_route')
    # tried to build forts on some islands
    cut(A, 24.0, lambda dur: SM.route_map(dur,
        [(0, 72.9, 10.9, 6.0), (dur, 73.45, 10.82, 2.4)],
        markers=[(73.68, 10.82, 2.0, (255, 140, 110), 14, True), (72.73, 11.12, 3.4, (255, 140, 110), 12, True)],
        labels=[('FORTS', 73.68, 10.82, 2.6, 6.0, 30, -20)], extra=('mid_north',), dim=0.12), 'dissolve', 0.9, 'sepia', 'forts_map')
    # the locals did not stay quiet
    cut(A, 30.15, vid('mk:48525', ss=3.0, zoom=(1.0, 1.1)), 'whip', 0.35, 'storm', 'waves_rocks')
    # poison story
    cut(A, 32.2, vid('mk:36797', ss=1.0, zoom=(1.0, 1.12), fx=[dust(0.15, 43, 30)]), 'dissolve', 1.0, 'dusk', 'dusk_boats')
    cut(A, 36.0, vid('mk:4202', ss=0.5, zoom=(1.0, 1.08)), 'dissolve', 1.0, 'dusk', 'magenta_coast')
    # difficult to say story or history
    cut(A, 40.05, vid('mk:1197', ss=2.0, zoom=(1.0, 1.08), fx=[dust(0.2, 44, 40)]), 'dissolve', 1.0, 'cold', 'pier_mist')
    # they did not easily accept the domination of outsiders
    cut(A, 42.6, vid('mk:49186', ss=0.5, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'teal', 'standing_firm')
    cut(A, 45.9, vid('mk:47139', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'warm', 'fisherman_dusk')
    # Tipu Sultan
    cut(A, 48.9, img('fl:59', 1.0, 1.16, (0.5, 0.55), (0.5, 0.45), fx=[dust(0.15, 45, 30)]), 'dissolve', 0.9, 'sepia', 'tipu_palace')
    # British
    cut(A, 52.5, vid('mk:34516', ss=0.5, zoom=(1.0, 1.1)), 'dissolve', 0.9, 'sepia', 'ship_ropes')
    # Madras Presidency
    cut(A, 55.7, lambda dur: SM.route_map(dur,
        [(0, 76.0, 11.5, 14.0), (dur, 76.5, 12.0, 11.0)],
        routes=[dict(pts=[LAK, (75.0, 11.5), (77.5, 12.2), MADRAS], t0=0.4, t1=3.4, color=(255, 214, 120), width=3)],
        markers=[(LAK[0], LAK[1], 0.2, (130, 235, 255), 10, True), (MADRAS[0], MADRAS[1], 3.2, (255, 225, 150), 12, True)],
        labels=[('MADRAS PRESIDENCY', MADRAS[0], MADRAS[1], 3.2, 6.0, -190, 36)]), 'dissolve', 0.9, 'sepia', 'madras')
