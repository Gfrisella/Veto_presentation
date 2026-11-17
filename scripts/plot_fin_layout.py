"""Layout of the example fin designs (R2-fins / R3-fins): top view and front view of the UBT and one fin pair."""
import json, sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import numpy as np
sys.path.insert(0, "/disk/data1/hep/gfrise/.claude-config/skills/cern-ship-slides/theme")
from plotstyle import C1, C2, C3, save

ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "designs/R2f_fins_ubt.json"))
fins = [f for f in d["fins"] if f["side"] == "left"]
Z_IN, Z_OUT, X_IN, X_OUT, Y_IN, Y_OUT = 31.13, 81.13, 0.5, 2.0, 1.35, 3.0
hw = lambda z: X_IN + (X_OUT - X_IN) * (z - Z_IN) / (Z_OUT - Z_IN)
hh = lambda z: Y_IN + (Y_OUT - Y_IN) * (z - Z_IN) / (Z_OUT - Z_IN)
GREEN, PURPLE = "#1b7f3b", "#7a3fb0"

fig, (a, b) = plt.subplots(1, 2, figsize=(15, 5.5), gridspec_kw=dict(width_ratios=[1.7, 1]))
# top view
a.add_patch(Polygon([[Z_IN, X_IN], [Z_OUT, X_OUT], [Z_OUT, -X_OUT], [Z_IN, -X_IN]], fill=False, ec="0.5", lw=1.5))
a.axhline(-4.56, color="#6b5a48", ls="--", lw=1.2); a.text(82.5, -4.4, "cavern wall", ha="right", fontsize=11, color="#6b5a48")
a.plot([30.73, 30.73], [-0.5, 0.5], color=C1, lw=4, label="UBT straws (30.73 m)")
a.plot([31.13, 31.13], [-1.7, 1.7], color=C1, lw=4, alpha=0.45, label="UBT tiles 3.4 m (31.13 m)")
a.plot([31.13, 31.13], [-2, 2], color="0.4", lw=1, ls=":", label="old tiles 4 m")
for f in fins:
    w = hw(f["z"])
    for s in (1, -1):
        a.plot([f["z"], f["z"]], [s * w, s * (w + f["length"])], color=C2, lw=4, solid_capstyle="butt")
    a.text(f["z"], w + f["length"] + 0.25, f"{f['z']:.2f}", ha="center", fontsize=10)
a.plot([], [], color=C2, lw=4, label="straw fins, 2 m reach")
for zl in (29.39, 29.59, 29.79):
    for s in (1, -1):
        a.plot([zl, zl], [s * 0.75, s * 1.35], color=GREEN, lw=3)
a.plot([], [], color=GREEN, lw=3, label="Si strips in MS7 (R3-fins)")
a.set_xlim(28.5, 83); a.set_ylim(-5, 5.2); a.set_xlabel("z [m]"); a.set_ylabel("x [m]")
a.set_title("Top view: 7 fins per side, $\\Delta z$ = 8.25 m"); a.legend(loc="lower left", ncol=2, fontsize=10, frameon=True)
a.grid(alpha=0.3)
# front view at the last fin
f = fins[-1]; w, h = hw(f["z"]), hh(f["z"])
for s in (1, -1):
    x0 = w if s > 0 else -(w + f["length"])
    for i in range(int(f["length"])):
        for y in np.arange(f["y_lo"], f["y_hi"] - 1e-9, 1.0):
            b.add_patch(Rectangle((x0 + i, y), 1, 1, fc="#fbe6d6", ec=C2, lw=1))
            for deg in (0, 15, -15):
                t = np.tan(np.radians(deg))
                for k in np.arange(0.1, 1.0, 0.2):
                    xs = np.array([x0 + i + k - 0.5 * t, x0 + i + k + 0.5 * t]); ys = np.array([y, y + 1])
                    xs = np.clip(xs, x0 + i, x0 + i + 1)
                    b.plot(xs, ys, color=C2, lw=0.5, alpha=0.6)
b.add_patch(Rectangle((-w, -h), 2 * w, 2 * h, fill=False, ec="0.5", lw=1.5))
b.text(0, 0, "vessel\n4.0 × 6.0 m", ha="center", va="center", fontsize=11, color="0.35")
b.axhline(-3.36, color="#6b5a48", ls="--", lw=1.2); b.axvline(-4.56, color="#6b5a48", ls="--", lw=1.2)
b.set_xlim(-5, 5); b.set_ylim(-3.6, 3.6); b.set_aspect("equal"); b.set_xlabel("x [m]"); b.set_ylabel("y [m]")
b.set_title(f"Front view at z = {f['z']:.2f} m: 1×1 m straw modules")
fig.tight_layout()
save(fig, ROOT / "figs/fins/fin_layout.png")
print("ok")
