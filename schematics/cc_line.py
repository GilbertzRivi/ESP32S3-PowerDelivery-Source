# One CC line (CC1). CC2 is identical: GPIO13 / GPIO14 / GPIO10 / GPIO17, own Rp legs on GPIO3 / GPIO8.
from common import *
with schemdraw.Drawing(file='cc_line.svg', show=False) as d:
    d.config(bgcolor='white')
    R = Point((0, 0))
    d += elm.Dot().at(R).label('CC1\n(receptacle)', loc='top')
    d += elm.Capacitor().at(R).down().length(2).label('2.2n', loc='bottom')
    d += elm.Ground()
    d += (qp := elm.NFet().theta(90).anchor('drain').at((1.8, 0)).label('2N7000', loc='bottom', ofst=0.1))
    W(d, R, qp.drain)
    d += elm.Line().at(qp.gate).up().length(1.0).label('node G', loc='end')
    S = qp.source
    cc = Point((S.x + 1.2, 0))
    d += elm.Dot().at(cc).label("CC1'", loc='bottom')
    # Rp legs
    for x, r, g in [(5.6, '12.2k', 'GPIO3\n(1.5 A)'), (7.4, '5.1k', 'GPIO8\n(3 A)')]:
        d += elm.Dot().at((x, 0))
        d += elm.Resistor().at((x, 0)).up().length(2.2).label(r)
        d += elm.Schottky().up().reverse().length(1.6).label('BAT85')
        d += elm.Line().up().length(0.4).label(g, loc='end')
    # TX high
    d += elm.Dot().at((9.2, 0))
    d += elm.Resistor().at((9.2, 0)).up().length(2.2).label('220R')
    d += elm.Line().up().length(2.0).label('GPIO11\nTX high', loc='end')
    # TX low
    d += elm.Resistor().at((9.2, 0)).down().length(2.0).label('122R', loc='bottom')
    d += (q := elm.BjtNpn(circle=True).theta(0).anchor('collector').label('BC547', loc='right', ofst=(0.1, 0.3)))
    d += elm.Line().at(q.emitter).down().length(0.6).label('E_CC', loc='end')
    d += elm.Resistor().at(q.base).left().length(2.2).label('2.2k')
    d += (tb := elm.Dot())
    d += (l12 := elm.Line().left().length(1.0))
    lab(d, l12.end, 'GPIO12\nTX low', loc='left')
    d += elm.Resistor().at(tb.center).down().length(1.8).label('10k', loc='bottom')
    d += elm.Ground()
    # ADC
    d += elm.Dot().at((11.4, 0))
    d += elm.Line().at((11.4, 0)).up().length(4.2).label('GPIO9\nADC', loc='end')
    # RX
    xr = 13.4
    d += elm.Resistor().at((xr, 0)).down().length(2.6).label('10k', loc='top')
    inp = Point((xr, -2.6))
    d += (op := elm.Opamp(leads=True).right().flip().anchor('in2').at((xr + 1.6, -2.6)).label('LM311', loc='center', ofst=(-0.3, 0)))
    fb = Point((xr + 0.7, -2.6))
    W(d, inp, op.in2)
    d += elm.Dot().at(fb)
    d += (lv := elm.Line().at(op.in1).left().length(1.8))
    lab(d, lv.end, 'Vref\n0.55 V', loc='left')
    A = Point((op.out.x + 0.5, op.out.y))
    W(d, op.out, A)
    d += elm.Dot().at(A)
    W(d, A, (A.x, -1.2))
    d += elm.Resistor().at((A.x, -1.2)).left().to((fb.x, -1.2)).label('330k')
    W(d, (fb.x, -1.2), fb)
    B = Point((A.x + 1.4, A.y))
    W(d, A, B)
    d += elm.Dot().at(B)
    d += elm.Resistor().at(B).up().length(1.8).label('1k')
    d += elm.Vdd().label('3V3')
    d += elm.Line().at(B).right().length(1.0).label('GPIO18\nRX (RMT)', loc='end')
    # bus
    W(d, S, (xr, 0))
