# Schematics

Drawn in Python with [Schemdraw](https://schemdraw.readthedocs.io/), one script per block.
The SVGs are committed, so you only need this if you want to change something.

| Script             | Block                                              |
|--------------------|----------------------------------------------------|
| `cc_line.py`       | One CC line: Rp, TX, RX, ADC, 2N7000, 2.2 nF       |
| `boost.py`         | Ground offset boost on GPIO6                       |
| `cc_protection.py` | 2N7000 pass transistors and the replica (node G)   |
| `vconn.py`         | VCONN switch, one per CC line                      |
| `vbus_switch.py`   | Back to back IRLZ44N, gate drive, bleeder, TVS     |

`common.py` only has small helpers shared by the scripts.
The descriptions and the reasons behind the values are in [docs/hardware.md](../docs/hardware.md).
