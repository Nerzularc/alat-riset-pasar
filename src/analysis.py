"""Pengambilan data dan analisis pasar."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

GEO_CODES = {"indonesia": "ID", "malaysia": "MY", "singapura": "SG", "global": ""}
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _timeframe(periode: str) -> str:
    """'2022-2025' -> '2022-01-01 2025-12-31' (format pytrends)."""
    start, end = periode.split("-")
    return f"{start}-01-01 {end}-12-31"


def fetch_trends(produk: str, lokasi: str, periode: str) -> tuple[pd.Series, pd.Series]:
    """Ambil minat pencarian dari Google Trends. Mengembalikan (time series, minat per wilayah)."""
    from pytrends.request import TrendReq

    geo = GEO_CODES.get(lokasi.lower(), lokasi.upper())
    py = TrendReq(hl="id-ID", tz=-420)
    py.build_payload([produk], timeframe=_timeframe(periode), geo=geo)
    over_time = py.interest_over_time()
    if over_time.empty:
        raise ValueError(f"Google Trends tidak punya data untuk '{produk}'.")
    regions = py.interest_by_region(resolution="REGION", inc_low_vol=False)[produk]
    return over_time[produk], regions


def load_demo() -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """Data contoh (dummy) untuk mencoba alat tanpa internet."""
    trend = pd.read_csv(DATA_DIR / "demo_trend.csv", parse_dates=["tanggal"]).set_index("tanggal")["minat"]
    regions = pd.read_csv(DATA_DIR / "demo_regions.csv").set_index("wilayah")["minat"]
    return trend, regions, load_competitors(DATA_DIR / "demo_competitors.csv")


def load_competitors(path: str | Path) -> pd.DataFrame:
    """CSV pesaing dengan kolom wajib: nama, harga. Kolom opsional: rating, terjual."""
    df = pd.read_csv(path)
    missing = {"nama", "harga"} - set(df.columns)
    if missing:
        raise ValueError(f"Kolom wajib tidak ada di CSV pesaing: {sorted(missing)}")
    return df


def analyze_trend(series: pd.Series) -> dict:
    """Bandingkan rata-rata 3 bulan pertama vs 3 bulan terakhir, plus puncak minat."""
    monthly = series.resample("MS").mean().dropna()
    if len(monthly) < 6:
        raise ValueError("Butuh minimal 6 bulan data untuk analisis tren.")
    awal, akhir = monthly.iloc[:3].mean(), monthly.iloc[-3:].mean()
    perubahan = (akhir - awal) / awal * 100 if awal else float("nan")
    return {
        "perubahan_persen": round(perubahan, 1),
        "arah": "naik" if perubahan > 5 else "turun" if perubahan < -5 else "stabil",
        "puncak_bulan": monthly.idxmax().strftime("%Y-%m"),
        "puncak_nilai": round(float(monthly.max()), 1),
    }


def top_regions(regions: pd.Series, n: int = 5) -> list[tuple[str, int]]:
    top = regions[regions > 0].sort_values(ascending=False).head(n)
    return [(str(k), int(v)) for k, v in top.items()]


def analyze_competitors(df: pd.DataFrame, n: int = 3) -> dict:
    sort_col = "terjual" if "terjual" in df.columns else "harga"
    top = df.sort_values(sort_col, ascending=False).head(n)
    return {
        "jumlah": len(df),
        "harga_min": int(df["harga"].min()),
        "harga_median": int(df["harga"].median()),
        "harga_max": int(df["harga"].max()),
        "urut_berdasarkan": sort_col,
        "top": top.to_dict(orient="records"),
    }
