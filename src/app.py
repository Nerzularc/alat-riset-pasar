"""Entrypoint CLI Alat Riset Pasar Digital."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import analysis
import visualization

ROOT = Path(__file__).resolve().parent.parent


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Alat riset pasar digital (tren + pesaing).")
    p.add_argument("--produk", required=True, help='Kata kunci produk, mis. "sepatu olahraga"')
    p.add_argument("--lokasi", default="Indonesia", help="Indonesia / Malaysia / Singapura / Global / kode ISO")
    p.add_argument("--periode", default="2022-2025", help="Rentang tahun, mis. 2022-2025")
    p.add_argument("--pesaing", help="Path CSV pesaing (kolom: nama, harga, [rating], [terjual])")
    p.add_argument("--output", default=str(ROOT / "output"), help="Folder hasil")
    p.add_argument("--demo", action="store_true", help="Pakai data contoh offline (bukan data nyata)")
    args = p.parse_args(argv)
    if not re.fullmatch(r"\d{4}-\d{4}", args.periode):
        p.error("--periode harus berformat YYYY-YYYY")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    competitors = None

    if args.demo:
        series, regions, competitors = analysis.load_demo()
        sumber = "DATA CONTOH (dummy) — bukan data pasar nyata"
    else:
        try:
            series, regions = analysis.fetch_trends(args.produk, args.lokasi, args.periode)
        except Exception as e:  # jaringan / rate limit Google Trends
            print(f"Gagal mengambil Google Trends: {e}", file=sys.stderr)
            return 1
        sumber = "Google Trends"
    if args.pesaing:
        competitors = analysis.load_competitors(args.pesaing)
        sumber += f" + {Path(args.pesaing).name}"

    trend = analysis.analyze_trend(series)
    top = analysis.top_regions(regions)
    comp = analysis.analyze_competitors(competitors) if competitors is not None else None

    out = Path(args.output) / re.sub(r"[^a-z0-9]+", "-", args.produk.lower()).strip("-")
    out.mkdir(parents=True, exist_ok=True)
    visualization.plot_trend(series, args.produk, out / "tren.png")
    series.to_csv(out / "tren.csv")
    if competitors is not None:
        competitors.to_csv(out / "pesaing.csv", index=False)
    report = visualization.build_report(args.produk, args.lokasi, args.periode, trend, top, comp, sumber)
    (out / "laporan.md").write_text(report, encoding="utf-8")

    visualization.print_summary(args.produk, trend, top, comp)
    print(f"Laporan, grafik, dan CSV disimpan di '{out}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
