# CC protection: two 2N7000 pass transistors and a replica that sets their gates.
from common import *
with schemdraw.Drawing(file='cc_protection.svg', show=False) as d:
    d.config(bgcolor='white')
    yb = -1.6                       # gate bus between the two lines
    # CC1: gate down, CC2: gate up, both gates meet on the bus
    d += (q1 := elm.NFet().theta(-90).flip().anchor('drain').at((2.0, 0)).label('Qp1\n2N7000', loc='top', ofst=0.1))
    d += (q2 := elm.NFet().theta(90).anchor('drain').at((2.0, 2 * yb)).label('Qp2\n2N7000', loc='bottom', ofst=0.1))
    for q, y, n in [(q1, 0, '1'), (q2, 2 * yb, '2')]:
        d += elm.Dot().at((0, y)).label(f'CC{n} (receptacle)', loc='top', ofst=0.15)
        W(d, (0, y), q.drain)
        d += elm.Line().at(q.source).right().length(1.6)
        d += elm.Dot()
        lab(d, (q.source.x + 1.6, y), f"CC{n}' (ESP side:\nRp, TX, RX, ADC)", loc='right')
        W(d, q.gate, (q.gate.x, yb))
    d += elm.Dot().at((q1.gate.x, yb))
    xg = 10.5
    G = Point((xg, yb))
    W(d, (q1.gate.x, yb), G)
    d += elm.Dot().at(G)
    d += elm.Label().at((6.6, yb)).label('node G (~5.3 V)', loc='top', ofst=0.15)
    # 100n on node G
    cn = Point((xg - 1.5, yb))
    d += elm.Dot().at(cn)
    d += elm.Capacitor().at(cn).down().length(1.4).label('100n', loc='bottom')
    d += elm.Ground()
    # 100k from +27 V
    d += elm.Line().at(G).up().length(0.6)
    d += elm.Resistor().up().length(2.0).label('100k')
    d += elm.Vdd().label('+27 V')
    # replica Qr, gate tied to drain
    d += (qr := elm.NFet().theta(0).anchor('drain').at((xg, yb - 0.6)))
    W(d, G, qr.drain)
    gd = Point((qr.gate.x + 0.5, qr.gate.y))
    W(d, qr.gate, gd); W(d, gd, (gd.x, yb)); W(d, G, (gd.x, yb))
    lab(d, (gd.x + 1.4, qr.gate.y), 'Qr 2N7000\ngate tied\nto drain', loc='right', ofst=0.1)
    d += elm.Resistor().at(qr.source).down().length(1.8).label('15k', loc='bottom')
    d += elm.Ground()
