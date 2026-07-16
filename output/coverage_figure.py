"""Render the data-store coverage heatmap for the README.

Reads output.json and jacob_ladder.json, counts calculation records per
(molecule, method rung), and writes
  images/data_store_coverage.png  (the figure)
  coverage_matrix.csv             (the same matrix as a table)

Run from the output/ directory:  python coverage_figure.py
"""
import csv
import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap

INK = "#1f1f1e"
MUTED = "#6b6a66"
EMPTY = "#f5f4f1"  # "no records" cell, distinct from the ramp
RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

with open("output.json") as f:
    data = json.load(f)
with open("../jacob_ladder.json") as f:
    ladder = json.load(f)

method_rung = {m.upper(): int(r) for r, ms in ladder.items() for m in ms}
molecules = sorted(data)
rows = [f"Rung {i}" for i in range(1, 10)] + ["WFT / MP2 ref"]
counts = np.zeros((len(rows), len(molecules)), dtype=int)

for j, mol in enumerate(molecules):
    for rec in data[mol]:
        if rec["method_type"] in ("wft", "rmp2"):
            counts[9, j] += 1
            continue
        rung = rec.get("method_level") or method_rung.get(str(rec["method"]).upper())
        if rung:
            counts[int(rung) - 1, j] += 1

total = int(counts.sum())
vmax = int(counts.max())

cmap = LinearSegmentedColormap.from_list("seq_blue", RAMP)
cmap.set_under(EMPTY)
norm = BoundaryNorm(np.arange(0.5, vmax + 1.5), cmap.N)

fig, ax = plt.subplots(figsize=(13.5, 3.9), dpi=200)
mesh = ax.pcolormesh(
    counts, cmap=cmap, norm=norm, edgecolors="white", linewidth=1.4, rasterized=True
)
ax.set_xticks(np.arange(len(molecules)) + 0.5)
ax.set_xticklabels(molecules, rotation=90, fontsize=5.4, color=INK)
ax.set_yticks(np.arange(len(rows)) + 0.5)
ax.set_yticklabels(rows, fontsize=8, color=INK)
ax.invert_yaxis()
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title(
    f"Coverage of the calculation data store: {total:,} records, "
    f"{len(molecules)} species, Jacob's-ladder rungs 1-9 + wavefunction references",
    fontsize=10.5, color=INK, loc="left", pad=12,
)

cbar = fig.colorbar(mesh, ax=ax, shrink=0.9, pad=0.01, ticks=range(1, vmax + 1))
cbar.ax.tick_params(labelsize=7, length=0, labelcolor=MUTED)
cbar.outline.set_visible(False)
cbar.set_label("records per cell (white = none)", fontsize=8, color=MUTED)

fig.tight_layout()
fig.savefig("images/data_store_coverage.png", facecolor="white", bbox_inches="tight")

with open("coverage_matrix.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rung"] + molecules)
    for label, row in zip(rows, counts):
        w.writerow([label] + row.tolist())
print(f"wrote images/data_store_coverage.png and coverage_matrix.csv "
      f"({total} records, vmax {vmax})")
