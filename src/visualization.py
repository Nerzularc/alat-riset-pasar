"""Grafik dan laporan."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def rupiah(x: float) -> str:
    return "Rp" + f"{int(x):,}".replace(",", ".")


def plot_trend(series: pd.Series, produk: str, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 4))
    series.plot(ax=ax, color="#1f6feb", linewidth=1.8)
    ax.set_title(f"Minat pencarian: {produk}")
    ax.set_ylabel("Indeks minat (0–100)")
    ax.set_xlabel("")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def build_report(produk, lokasi, periode, trend, regions, comp, sumber) -> str:
    lines = [
        f"# Ringkasan Riset Pasar: {produk}",
        "",
        f"- **Wilayah:** {lokasi}  ",
        f"- **Periode:** {periode}  ",
        f"- **Sumber data:** {sumber}  ",
        f"- **Dibuat:** {date.today().isoformat()}",
        "",
        "## Tren Permintaan",
        f"Minat pencarian **{trend['arah']}** {trend['perubahan_persen']:+}% "
        f"(rata-rata 3 bulan awal vs 3 bulan akhir). "
        f"Puncak di {trend['puncak_bulan']} (indeks {trend['puncak_nilai']}).",
        "",
        "![Grafik tren](tren.png)",
        "",
    ]
    if regions:
        lines += ["## Wilayah dengan Minat Tertinggi", "", "| Wilayah | Indeks |", "|---|---|"]
        lines += [f"| {r} | {v} |" for r, v in regions]
        lines.append("")
    if comp:
        lines += [
            "## Pesaing",
            f"{comp['jumlah']} produk dianalisis. Rentang harga {rupiah(comp['harga_min'])}–"
            f"{rupiah(comp['harga_max'])}, median {rupiah(comp['harga_median'])}.",
            "",
            f"Top {len(comp['top'])} berdasarkan **{comp['urut_berdasarkan']}**:",
            "",
            "| Nama | Harga | Rating | Terjual |",
            "|---|---|---|---|",
        ]
        for c in comp["top"]:
            lines.append(f"| {c['nama']} | {rupiah(c['harga'])} | {c.get('rating', '-')} | {c.get('terjual', '-')} |")
        lines.append("")
    return "\n".join(lines)


def print_summary(produk, trend, regions, comp) -> None:
    print(f"=== Ringkasan Riset Pasar '{produk}' ===")
    print(f"- Tren Permintaan: {trend['arah']} {trend['perubahan_persen']:+}% (puncak {trend['puncak_bulan']})")
    if regions:
        print("- Wilayah teratas: " + ", ".join(r for r, _ in regions[:3]))
    if comp:
        top = ", ".join(f"{c['nama']} ({rupiah(c['harga'])})" for c in comp["top"])
        print(f"- Top Pesaing: {top}")
        print(f"- Range Harga Pasar: {rupiah(comp['harga_min'])}–{rupiah(comp['harga_max'])}")
