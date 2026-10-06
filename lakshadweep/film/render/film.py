import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film_core as FC
from engine import Timeline, write_range, FPS
import importlib


def build_timeline(acts=(1, 2, 3, 4, 5, 6, 7, 8)):
    FC.ENTRIES.clear(); FC.TAGS.clear(); FC.OVERLAYS.clear()
    for a in acts:
        importlib.import_module(f'act{a}').build()
    FC.OVERLAYS.insert(0, FC.act_dips) if FC.act_dips not in FC.OVERLAYS else None
    tl = Timeline(FC.ENTRIES, FC.TOTAL, subs=FC.subs(), tags=FC.TAGS, overlays=FC.OVERLAYS)
    return tl


if __name__ == '__main__':
    pass
