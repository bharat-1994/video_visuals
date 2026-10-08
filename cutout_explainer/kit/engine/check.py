import sys, importlib, cairo
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.getcwd())
from lib import W,H
m=importlib.import_module(sys.argv[1]); fn=getattr(m,sys.argv[2]); t=float(sys.argv[3])
dur=dict((f.__name__,d) for d,f in m.SCENES)[sys.argv[2]]
s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s); c.set_source_rgb(1,1,1); c.paint(); fn(c,t,dur); s.write_to_png(sys.argv[4])
