"""Regenerate example figures for the SoftDFT website from saved example data.

Usage:  python _build/make_figures.py <path-to-Research/example>
Writes PNGs into assets/img/examples/.
"""
import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

EX = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "examples"
OUT.mkdir(parents=True, exist_ok=True)

C = ["#8C0B42", "#2F5D8A", "#C07A12", "#2A7F6F", "#6B5B95", "#555555"]
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
    "axes.spines.right": False, "axes.edgecolor": "#444", "axes.labelcolor": "#222",
    "xtick.color": "#444", "ytick.color": "#444", "legend.frameon": False,
    "figure.dpi": 160, "savefig.bbox": "tight", "axes.grid": True,
    "grid.color": "#e6e3dc", "grid.linewidth": 0.7,
})


def read(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return {k: [float(r[k]) for r in rows] for k in rows[0]}


def fig(name, draw, size=(6.4, 3.8)):
    f, ax = plt.subplots(figsize=size)
    draw(ax)
    f.savefig(OUT / name)
    plt.close(f)
    print("wrote", name)


def d(n):
    return next(EX.glob(f"{n}_example_*"))


# 1 ideal gas
def ex1(ax):
    t = read(d(1) / "data/comparison.csv")
    ax.plot(t["z_over_d"], t["exact_ideal_density"], color="#bbb", lw=5, label="exact Boltzmann")
    ax.plot(t["z_over_d"], t["softdft_density"], color=C[0], lw=1.6, ls="--", label="SoftDFT")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$"); ax.legend()
fig("ex01_ideal_gas.png", ex1)


# 5 hard-sphere wall
def ex5(ax):
    t = read(d(5) / "data/comparison.csv")
    ax.plot(t["z_over_d"], t["softdft_over_bulk"], color=C[0], lw=1.6)
    ax.axhline(1, color="#999", lw=0.8)
    ax.set_xlim(0, 6); ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho(z)/\rho_b$")
    ax.set_title(r"hard spheres, $\rho_b d^3 = 0.305$", fontsize=10, loc="left")
fig("ex05_hs_wall.png", ex5)


# 7 cross-dimension
def ex7(ax):
    t = read(d(7) / "data/profiles.csv")
    ax.plot(t["z_over_d"], t["rho_1d"], color="#bbb", lw=6, label="1D")
    ax.plot(t["z_over_d"], t["rho_2d"], color=C[1], lw=2.2, ls="--", label="2D (lateral avg.)")
    ax.plot(t["z_over_d"], t["rho_3d"], color=C[0], lw=1.2, ls=":", label="3D (lateral avg.)")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$"); ax.legend()
fig("ex07_cross_dimension.png", ex7)


# 8 neutral brush
def ex8(ax):
    t = read(d(8) / "data/profiles.csv")
    ax.plot(t["z_over_d"], t["rho_polymer_beads"], color=C[0], lw=1.8, label="polymer beads")
    ax.plot(t["z_over_d"], t["rho_solvent"], color=C[1], lw=1.8, label="solvent")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$"); ax.legend()
fig("ex08_neutral_brush.png", ex8)


# 10 electrolyte charged slit
def ex10(ax):
    t = read(d(10) / "data/profiles.csv")
    ax.plot(t["z_over_d"], t["rho_c"], color=C[0], lw=1.8, label="cation")
    ax.plot(t["z_over_d"], t["rho_a"], color=C[1], lw=1.8, label="anion")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$")
    a2 = ax.twinx(); a2.grid(False); a2.spines["right"].set_visible(True)
    a2.plot(t["z_over_d"], t["dimensionless_potential"], color=C[2], lw=1.2, ls="--", label=r"$\beta e\psi$")
    a2.set_ylabel(r"$\beta e \psi$")
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper center")
fig("ex10_charged_slit.png", ex10)


# 11 charge reversal
def ex11(ax):
    t = read(d(11) / "data/profiles.csv")
    ax.plot(t["z_over_d"], t["c_negative"], color=C[0], lw=1.8, label="cation, walls −")
    ax.plot(t["z_over_d"], t["a_positive"], color="#f0a0bf", lw=1.0, ls="--", label="anion, walls +")
    ax.plot(t["z_over_d"], t["a_negative"], color=C[1], lw=1.8, label="anion, walls −")
    ax.plot(t["z_over_d"], t["c_positive"], color="#9dc0e3", lw=1.0, ls="--", label="cation, walls +")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$"); ax.legend(ncol=2, fontsize=9, loc="lower center")
fig("ex11_charge_reversal.png", ex11)


# 12 asymmetric 2:1
def ex12(ax):
    t = read(d(12) / "data/profiles.csv")
    ax.plot(t["z_over_d"], t["rho_c_charged"], color=C[0], lw=1.8, label="+2 cation, charged walls")
    ax.plot(t["z_over_d"], t["rho_a_charged"], color=C[1], lw=1.8, label="−1 anion, charged walls")
    ax.plot(t["z_over_d"], t["rho_c_neutral"], color=C[0], lw=1, ls=":", label="+2 cation, neutral walls")
    ax.plot(t["z_over_d"], t["rho_a_neutral"], color=C[1], lw=1, ls=":", label="−1 anion, neutral walls")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$"); ax.legend(fontsize=9, ncol=2, loc="lower center")
fig("ex12_asymmetric_electrolyte.png", ex12)


# 13 two-step acid
def ex13(ax):
    t = read(d(13) / "data/equilibrium.csv")
    w = 0.25
    for i, (k, lab) in enumerate([("A", "A (0)"), ("B", "B (−1)"), ("C", "C (−2)")]):
        xs = [p + (i - 1) * w for p in range(3)]
        ax.bar(xs, t[f"{k}_observed"], width=w, color=C[i], label=lab)
        ax.scatter(xs, t[f"{k}_ideal"], color="k", s=14, zorder=3)
    ax.set_xticks(range(3), [f"pH {int(p)}" for p in t["pH"]])
    ax.set_ylabel("state fraction"); ax.legend(title="bars: SoftDFT · dots: mass action", fontsize=9, title_fontsize=9)
fig("ex13_two_step_acid.png", ex13)


# 14 charge-regulating brush
def ex14(ax):
    t = read(d(14) / "data/profiles.csv")
    ax.plot(t["z_over_d"], t["rho_A"], color=C[3], lw=1.8, label="A (neutral)")
    ax.plot(t["z_over_d"], t["rho_B"], color=C[0], lw=1.8, label="B (ionized)")
    ax.plot(t["z_over_d"], t["rho_c"], color=C[2], lw=1.4, label="cation")
    ax.plot(t["z_over_d"], t["rho_a"], color=C[1], lw=1.4, label="anion")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$"); ax.legend()
fig("ex14_regulating_brush.png", ex14)


# 15 pH / salt sweep
def ex15(ax):
    t = read(d(15) / "data/sweep_summary.csv")
    for s, col in [(0.01, C[1]), (0.05, C[0])]:
        idx = [i for i, v in enumerate(t["salt_reduced"]) if abs(v - s) < 1e-9]
        ax.plot([t["pH"][i] for i in idx], [t["ionized_fraction"][i] for i in idx], "o-", color=col,
                label=fr"salt $\rho d^3$ = {s}")
    ax.set_xlabel("pH"); ax.set_ylabel("mean ionized fraction"); ax.set_xticks([5, 7]); ax.legend()
fig("ex15_ph_salt_sweep.png", ex15, size=(5.2, 3.6))


# 17 square-well adsorption
def ex17(ax):
    t = read(d(17) / "data/profiles.csv")
    ax.plot(t["z_over_d"], t["A_attractive"], color=C[0], lw=1.8, label="A, attractive wall")
    ax.plot(t["z_over_d"], t["B_attractive"], color=C[1], lw=1.8, label="B, attractive wall")
    ax.plot(t["z_over_d"], t["A_control"], color=C[0], lw=1, ls=":", label="A, control")
    ax.plot(t["z_over_d"], t["B_control"], color=C[1], lw=1, ls=":", label="B, control")
    ax.set_xlabel("z / d"); ax.set_ylabel(r"$\rho\,d^3$"); ax.legend()
fig("ex17_square_well.png", ex17)


# 9 segment conservation: per-segment error for the 5-bead chain on three grids
def ex9(ax):
    with open(d(9) / "data/segment_amounts.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    for case, h, col in [("n5_h02", "0.2", C[0]), ("n5_h01", "0.1", C[2]), ("n5_h005", "0.05", C[1])]:
        r = [x for x in rows if x["case"] == case]
        ax.plot([int(x["segment"]) for x in r], [100 * float(x["relative_error"]) for x in r], "o-",
                color=col, label=f"grid spacing {h}d")
    ax.set_xticks(range(1, 6)); ax.set_xlabel("segment (1 = grafted end)")
    ax.set_ylabel("segment-amount error (%)"); ax.legend()
fig("ex09_segment_conservation.png", ex9)
