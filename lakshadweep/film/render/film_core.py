"""Timeline collection helpers shared by act modules."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'build'))
from timeline import ACTS, START, SEG, TOTAL, PRE
from engine import Entry

ENTRIES = []
TAGS = []
OVERLAYS = []


def GT(act, local):
    """act (1..8), act-local seconds -> global seconds"""
    return START[ACTS[act - 1]] + local


def cut(act, local, factory, trans='dissolve', tdur=0.9, grade='teal', name=''):
    ENTRIES.append(Entry(GT(act, local), factory, trans, tdur, grade, name))


def cutg(t, factory, trans='dissolve', tdur=0.9, grade='teal', name=''):
    ENTRIES.append(Entry(t, factory, trans, tdur, grade, name))


def tag(act, l0, l1, title, sub):
    TAGS.append((GT(act, l0), GT(act, l1), title, sub))


def subs():
    out = []
    for i, a in enumerate(ACTS):
        for s in SEG[a]['segs']:
            out.append((START[a] + s['start'], START[a] + s['end'], s['te']))
    return out


def act_dips(img, T):
    """chapter breaks: dip to black through the breathing gap between acts."""
    import numpy as np
    from engine import smooth
    for i, a in enumerate(ACTS[:-1]):
        end = START[a] + SEG[a]['duration']
        nxt = START[ACTS[i + 1]]
        if end - 1.0 <= T <= nxt + 0.7:
            if T < end - 1.0 + 1.0:
                al = smooth((T - (end - 1.0)) / 1.0)
            elif T < nxt:
                al = 1.0
            else:
                al = 1.0 - smooth((T - nxt) / 0.7)
            return (img.astype(np.float32) * (1 - al)).astype(np.uint8)
    # final outro fade handled in act8
    return img
