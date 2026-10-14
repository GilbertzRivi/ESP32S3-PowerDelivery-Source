# Shared helpers for the schematics. Needs schemdraw (pip install schemdraw), tested with 0.23.
import schemdraw, schemdraw.elements as elm
from schemdraw.util import Point
schemdraw.config(fontsize=11, lw=1.6)
def W(d, a, b, shape='-'):
    d += elm.Wire(shape).at(a).to(b)
def lab(d, p, text, loc='right', ofst=0.15):
    d += elm.Label().at(p).label(text, loc=loc, ofst=ofst)
