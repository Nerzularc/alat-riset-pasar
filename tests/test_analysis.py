import pandas as pd
import pytest

import analysis
import app


def _series(values):
    idx = pd.date_range("2024-01-01", periods=len(values), freq="MS")
    return pd.Series(values, index=idx, dtype=float)


def test_trend_naik():
    r = analysis.analyze_trend(_series([10, 10, 10, 15, 18, 20, 20, 20, 20]))
    assert r["arah"] == "naik"
    assert r["perubahan_persen"] == 100.0
    assert r["puncak_bulan"] == "2024-06"


def test_trend_stabil():
    assert analysis.analyze_trend(_series([50] * 8))["arah"] == "stabil"


def test_trend_data_kurang():
    with pytest.raises(ValueError):
        analysis.analyze_trend(_series([1, 2, 3]))


def test_competitors_urut_terjual():
    df = pd.DataFrame({"nama": ["A", "B", "C", "D"], "harga": [100, 300, 200, 400], "terjual": [5, 50, 20, 1]})
    r = analysis.analyze_competitors(df)
    assert [c["nama"] for c in r["top"]] == ["B", "C", "A"]
    assert (r["harga_min"], r["harga_median"], r["harga_max"]) == (100, 250, 400)


def test_competitors_kolom_wajib(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text("nama\nA\n")
    with pytest.raises(ValueError, match="harga"):
        analysis.load_competitors(f)


def test_demo_end_to_end(tmp_path):
    assert app.main(["--produk", "sepatu olahraga", "--demo", "--output", str(tmp_path)]) == 0
    out = tmp_path / "sepatu-olahraga"
    for name in ["laporan.md", "tren.png", "tren.csv", "pesaing.csv"]:
        assert (out / name).exists()
    assert "DATA CONTOH" in (out / "laporan.md").read_text()
