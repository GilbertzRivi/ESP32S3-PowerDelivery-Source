# VBUS switch: two IRLZ44N back to back, gate driven from +27 V, plus bleeder and TVS.
from common import *
with schemdraw.Drawing(file='vbus_switch.svg', show=False) as d:
    d.config(bgcolor='white')
    yg = 2.6                                    # gate bus
    d += elm.Dot().at((0, 0)).label('converter\nOUT+', loc='left')
    d += (q1 := elm.NFet().theta(90).anchor('drain').at((1.4, 0)))
    W(d, (0, 0), q1.drain)
    xs = q1.source.x + 2.4                      # common source node
    d += (q2 := elm.NFet().theta(90).flip().anchor('source').at((xs + 2.4, 0)))
    W(d, q1.source, q2.source)
    for q, n in [(q1, 'Q1'), (q2, 'Q2')]:
        d += elm.Label().at(((q.drain.x + q.source.x) / 2, -0.45)).label(n + ' IRLZ44N', loc='bottom', ofst=0)
    # zener and 100k between the gate bus and the sources
    d += elm.Dot().at((xs - 1.1, 0))
    d += elm.Zener().at((xs - 1.1, 0)).up().length(yg).label('12 V', loc='top')
    d += elm.Dot().at((xs + 1.1, 0))
    d += elm.Resistor().at((xs + 1.1, 0)).up().length(yg).label('100k', loc='bottom')
    W(d, q1.gate, (q1.gate.x, yg)); W(d, q2.gate, (q2.gate.x, yg))
    W(d, (q1.gate.x, yg), (q2.gate.x, yg))
    for x in (xs - 1.1, xs + 1.1):
        d += elm.Dot().at((x, yg))
    G = Point((xs, yg))
    d += elm.Dot().at(G)
    # high side: BC557 from +27 V through 10k into the gates
    d += elm.Resistor().at(G).up().length(2.2).label('10k')
    d += (qp := elm.BjtPnp(circle=True).theta(0).anchor('collector').label('BC557', loc='right', ofst=(0.1, 0.0)))
    ytop = qp.emitter.y + 0.6
    W(d, qp.emitter, (xs, ytop))
    d += elm.Vdd().at((xs, ytop)).label('+27 V')
    d += elm.Dot().at((xs, ytop))
    B = Point((xs - 4.2, qp.base.y))
    W(d, qp.base, B)
    d += elm.Dot().at(B)
    d += elm.Resistor().at(B).up().to((B.x, ytop)).label('10k')
    W(d, (B.x, ytop), (xs, ytop))
    # low side: BC547 from GPIO15
    d += elm.Resistor().at(B).down().length(1.8).label('10k')
    d += (qn := elm.BjtNpn(circle=True).theta(0).anchor('collector').label('BC547', loc='right', ofst=(0.1, 0.0)))
    d += elm.Ground().at(qn.emitter)
    N = Point((qn.base.x - 1.4, qn.base.y))
    W(d, qn.base, N)
    d += elm.Dot().at(N)
    d += elm.Resistor().at(N).down().length(1.6).label('10k', loc='bottom')
    d += elm.Ground()
    d += elm.Resistor().at(N).left().length(2.0).label('5.1k')
    d += (lg := elm.Line().left().length(0.5))
    lab(d, lg.end, 'GPIO15\n1 = on', loc='left')
    # VBUS side: bleeder, TVS, receptacle
    xv = q2.drain.x + 1.4
    W(d, q2.drain, (xv, 0))
    d += elm.Dot().at((xv, 0))
    d += elm.Resistor().at((xv, 0)).down().length(2.0).label('4.7k', loc='bottom')
    d += elm.Ground()
    xt = xv + 2.0
    W(d, (xv, 0), (xt, 0))
    d += elm.Dot().at((xt, 0))
    d += elm.Zener().at((xt, 0)).down().reverse().length(2.0).label('TVS\n1.5KE27A', loc='bottom')
    d += elm.Ground()
    d += elm.Line().at((xt, 0)).right().length(1.2)
    d += (o := elm.Dot())
    lab(d, o.center, 'VBUS\n(receptacle)', loc='right')
