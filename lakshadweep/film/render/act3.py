import film_core as FC
from film_core import cut, cutg, tag, GT
from shots import *
import scenes_misc as SM
from engine import smooth
import fx as FX

KANNUR = (75.37, 11.87); KOZHI = (75.78, 11.25); KOCHI = (76.27, 9.97)
KAVARATTI = (72.64, 10.57); AGATTI = (72.18, 10.86); AMINI = (72.73, 11.12); ANDROTH = (73.68, 10.82)


def build():
    A = 3
    # When did people first set foot...?
    cut(A, 0.0, img('fl:4', 1.0, 1.12, (0.55, 0.55), (0.45, 0.5), shake=0.3, fx=[fade_in(1.2), dust(0.2, 21, 40)]), 'dissolve', 0.01, 'dusk', 'first_steps')
    # no exact record -> mist
    cut(A, 2.94, vid('mk:1164', ss=6.0, speed=0.8, zoom=(1.0, 1.08), fx=[dust(0.2, 22, 50)]), 'dissolve', 1.0, 'cold', 'no_record')
    # oral stories and beliefs
    cut(A, 5.14, vid('mk:14341', ss=0.5, zoom=(1.0, 1.08)), 'dissolve', 1.0, 'warm', 'stories_canoe')
    cut(A, 8.3, img('fl:23', 1.0, 1.14, (0.5, 0.55), (0.5, 0.45), shake=0.3, fx=[dust(0.15, 23, 30)]), 'dissolve', 0.9, 'warm', 'local_at_work')
    # sailors and fishermen from the Kerala coast came and settled
    cut(A, 10.58, lambda dur: SM.route_map(dur,
        [(0, 74.0, 11.0, 5.0), (dur, 73.9, 10.9, 4.2)],
        routes=[dict(pts=[KANNUR, (74.4, 11.5), AMINI], t0=0.4, t1=3.0, color=(255, 214, 120)),
                dict(pts=[KOZHI, (74.2, 10.9), KAVARATTI], t0=1.0, t1=3.6, color=(255, 214, 120)),
                dict(pts=[KOCHI, (74.6, 10.3), AGATTI], t0=1.6, t1=4.2, color=(255, 214, 120))],
        markers=[(KANNUR[0], KANNUR[1], 0.2, (255, 225, 150), 8, True), (KOZHI[0], KOZHI[1], 0.8, (255, 225, 150), 8, True), (KOCHI[0], KOCHI[1], 1.4, (255, 225, 150), 8, True),
                 (AMINI[0], AMINI[1], 3.0, (130, 235, 255), 8, True), (KAVARATTI[0], KAVARATTI[1], 3.6, (130, 235, 255), 8, True), (AGATTI[0], AGATTI[1], 4.2, (130, 235, 255), 8, True)],
        labels=[('KERALA COAST', 76.0, 10.9, 0.6, 5.5, 20, -10)], extra=('mid_north',)), 'dissolve', 0.9, 'teal', 'route_kerala')
    cut(A, 14.1, img('fl:33', 1.0, 1.10, (0.5, 0.5), (0.45, 0.5), shake=0.4, fx=[dust(0.2, 24, 30)]), 'whip', 0.4, 'warm', 'trawlers')
    cut(A, 16.0, vid('mk:15622', ss=1.0, zoom=(1.0, 1.1), fx=[dust(0.1, 25, 25)]), 'dissolve', 0.8, 'teal', 'boat_out')
    # Arab traders: the Arabian Sea route
    cut(A, 17.98, lambda dur: SM.route_map(dur,
        [(0, 60.0, 17.0, 34.0), (dur, 64.0, 15.0, 28.0)],
        routes=[dict(pts=[(58.6, 23.6), (65.0, 19.0), (70.5, 14.0), (75.2, 11.4)], t0=0.2, t1=3.6, color=(255, 190, 110), width=4),
                dict(pts=[(45.0, 12.8), (55.0, 12.5), (65.0, 12.4), (73.0, 11.2), (75.4, 11.2)], t0=0.8, t1=4.2, color=(255, 190, 110), width=4)],
        markers=[(58.6, 23.6, 0.1, (255, 225, 150), 8, True), (45.0, 12.8, 0.6, (255, 225, 150), 8, True), (75.4, 11.3, 3.8, (130, 235, 255), 10, True)],
        labels=[('ARABIA', 52.0, 21.0, 0.8, 4.8, 0, 0), ('MALABAR', 75.4, 11.3, 3.8, 5.2, -190, 30)], layers=None), 'dissolve', 0.9, 'teal', 'route_arab')
    cut(A, 20.6, img('fl:50', 1.0, 1.10, (0.5, 0.55), (0.55, 0.5), shake=0.3, fx=[dust(0.15, 26, 30)]), 'dissolve', 0.8, 'warm', 'dhow_sur')
    cut(A, 22.1, img('fl:48', 1.0, 1.10, (0.5, 0.55), (0.45, 0.5), shake=0.4), 'dissolve', 0.8, 'warm', 'dhow_creek')
    # roadside stops on the sea route
    cut(A, 23.28, lambda dur: SM.route_map(dur,
        [(0, 73.2, 10.4, 7.0), (dur, 73.0, 10.3, 4.6)],
        routes=[dict(pts=[(70.0, 11.9), (71.5, 11.4), (72.7, 11.0), (74.2, 10.7), (75.5, 10.3)], t0=0.2, t1=4.8, color=(255, 214, 120), width=4)],
        markers=[(71.77, 12.28, 1.0, (130, 235, 255), 8, True), (72.18, 10.86, 1.9, (130, 235, 255), 8, True), (72.64, 10.57, 2.8, (130, 235, 255), 8, True), (73.04, 8.28, 3.6, (130, 235, 255), 8, True), (73.65, 10.08, 4.3, (130, 235, 255), 8, True)],
        extra=('mid_north',)), 'dissolve', 0.9, 'teal', 'route_stops')
    # Ubaidullah — reverent, warm, still
    cut(A, 28.52, img('fl:1', 1.0, 1.16, (0.5, 0.55), (0.5, 0.5), fx=[dust(0.3, 27, 50), fade_in(0.6)]), 'dissolve', 1.2, 'dusk', 'palms_dusk')
    cut(A, 32.2, vid('mk:1191', ss=3.0, zoom=(1.0, 1.08), fx=[dust(0.15, 28, 30)]), 'dissolve', 1.2, 'dusk', 'palm_sunset')
    # tomb at Androth
    cut(A, 35.85, lambda dur: SM.route_map(dur,
        [(0, 73.0, 10.9, 7.0), (dur, 73.6, 10.82, 2.4)],
        markers=[(ANDROTH[0], ANDROTH[1], 1.0, (255, 225, 150), 12, True)],
        labels=[('ANDROTH', ANDROTH[0], ANDROTH[1], 1.4, 4.8, 28, -4)], extra=('mid_north',), dim=0.1), 'dissolve', 1.0, 'dusk', 'androth_pin')
    # Islam spread: rings expand from Androth
    cut(A, 40.7, lambda dur: SM.route_map(dur,
        [(0, 73.6, 10.82, 2.4), (dur, 73.2, 10.6, 6.5)],
        markers=[(ANDROTH[0], ANDROTH[1], 0.0, (255, 225, 150), 16, True), (AMINI[0], AMINI[1], 1.0, (130, 235, 255), 8, True), (KAVARATTI[0], KAVARATTI[1], 1.4, (130, 235, 255), 8, True), (AGATTI[0], AGATTI[1], 1.8, (130, 235, 255), 8, True), (73.65, 10.08, 1.2, (130, 235, 255), 8, True)],
        extra=('mid_north',)), 'dissolve', 0.9, 'teal', 'spread')
    # almost 95% — community
    cut(A, 43.93, img('fl:13', 1.0, 1.10, (0.5, 0.5), (0.5, 0.45), shake=0.3, fx=[dust(0.15, 29, 30)]), 'dissolve', 0.9, 'warm', 'kids')
    cut(A, 46.1, img('fl:28', 1.0, 1.10, (0.5, 0.5), (0.5, 0.5), shake=0.3), 'dissolve', 0.8, 'warm', 'kids2')
    # coconut
    cut(A, 48.15, vid('mk:6910', ss=1.0, zoom=(1.0, 1.1), fx=[dust(0.2, 30, 30)]), 'dissolve', 0.8, 'warm', 'coconut_hang')
    cut(A, 50.2, vid('mk:7099', ss=1.0, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'warm', 'coconut_palms')
    # coir — rope from husk / resourcefulness
    cut(A, 52.8, vid('mk:4645', ss=2.0, zoom=(1.0, 1.1)), 'dissolve', 0.8, 'warm', 'palm_sun')
    cut(A, 55.0, img('fl:2', 1.0, 1.15, (0.5, 0.5), (0.5, 0.5), fx=[dust(0.1, 31, 30)]), 'dissolve', 0.8, 'warm', 'fish_sand')
    cut(A, 57.0, img('fl:6', 1.0, 1.15, (0.5, 0.5), (0.5, 0.5)), 'dissolve', 0.8, 'warm', 'coral_hand')
    cut(A, 59.4, img('fl:10', 1.0, 1.14, (0.45, 0.5), (0.5, 0.5), shake=0.3, fx=[fade_out(1.5)]), 'dissolve', 0.8, 'warm', 'boat_end')
