"""Example designs for the slides (NOT reference designs): R2 / R3 without the SBT, with 7 straw fins per side.

Fins: 7 per side, equispaced from the vessel exit (81.13 m) to 50 cm after the UBT tile plane (31.63 m), straw modules
(1 x 1 m, 3 stereo views) covering the vessel height at that z, reach L_FIN outwards from the side wall.
UBT: vertical-straw plane unchanged; tile plane 3.4 x 2.7 m^2 (|x| <= 1.7, |y| <= 1.35) instead of 4 x 4 m^2.
Usage: python3 make_fin_designs.py <path to veto/designs>   (reads R2 / R3 there, writes next to this script)
"""
import json, math, sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent
Z_IN, Z_OUT, Y_IN, Y_OUT = 31.13, 81.13, 1.35, 3.0
N_FIN, Z_FIRST, Z_LAST = 7, Z_IN + 0.5, Z_OUT
L_FIN = 2.0              # m outwards from the side wall (2 straw modules)
SLOT, Y0, MOD = 0.5, -3.0, 1.0


def half_height(z):
    return Y_IN + (Y_OUT - Y_IN) * (z - Z_IN) / (Z_OUT - Z_IN)


def fin(side, z):
    Y = half_height(z)
    iy0 = math.floor((-Y - Y0) / SLOT + 1e-9)
    ny = math.ceil((Y - (Y0 + iy0 * SLOT)) / MOD - 1e-9)
    nu = int(round(L_FIN / MOD))
    y_lo = Y0 + iy0 * SLOT                       # snapped to the 50 cm grid, whole 1 x 1 m straw modules
    return dict(side=side, z=round(z, 4), tilt=0, technology="straw", length=nu * MOD,
                y_lo=y_lo, y_hi=y_lo + ny * MOD, stations=1)


zs = [Z_FIRST + i * (Z_LAST - Z_FIRST) / (N_FIN - 1) for i in range(N_FIN)]
fins = [fin(s, z) for z in zs for s in ("right", "left")]
tiles = dict(half_x=1.7, y_lo=-1.35, y_hi=1.35)
common = (f"7 straw fins per side at z = {', '.join(f'{z:.2f}' for z in zs)} m (equispaced, vessel exit to 50 cm after the "
          f"UBT), {L_FIN:.0f} m reach, full vessel height; UBT tile plane 3.4 x 2.7 m^2; no SBT. Example design, not a reference.")
for src, name, label in (("R2_sbt_ubt", "R2f_fins_ubt", "R2 without the SBT, with fins"),
                         ("R3_sbt_ubt_strips", "R3f_fins_ubt_strips", "R3 without the SBT, with fins")):
    d = json.load(open(SRC / f"{src}.json"))
    d.pop("sbt", None)
    d.update(name=name, description=f"{label}: {common}", fins=fins, ubt_tiles=tiles)
    (OUT / f"{name}.json").write_text(json.dumps(d, indent=1))
    print("wrote", OUT / f"{name}.json", len(fins), "fins")
