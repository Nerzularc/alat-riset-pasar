# Alat Riset Pasar Digital

Alat riset pasar open-source berbasis Python untuk menganalisis **tren permintaan** (Google Trends), **wilayah dengan minat tertinggi**, dan **perbandingan harga pesaing**, lalu menyusun laporan otomatis berisi ringkasan, tabel, dan grafik.

![CI](https://github.com/USERNAME/alat-riset-pasar/actions/workflows/ci.yml/badge.svg)

## Fitur

- **Analisis tren**: minat pencarian Google Trends per periode, arah tren (naik/turun/stabil) dan bulan puncak.
- **Wilayah teratas**: provinsi/wilayah dengan minat pencarian tertinggi.
- **Analisis pesaing**: rentang dan median harga, plus top 3 produk (berdasarkan jumlah terjual jika ada).
- **Laporan otomatis**: `laporan.md`, grafik `tren.png`, dan data mentah CSV di folder `output/`.
- **Mode demo**: coba alat tanpa internet dengan data contoh.

## Instalasi

```bash
git clone https://github.com/USERNAME/alat-riset-pasar.git
cd alat-riset-pasar
pip install -r requirements.txt
```

Butuh Python 3.10+. Google Trends tidak memerlukan API key.

## Cara Penggunaan

```bash
# Coba dulu dengan data contoh (offline)
python src/app.py --produk "sepatu olahraga" --demo

# Data tren nyata dari Google Trends
python src/app.py --produk "sepatu olahraga" --lokasi Indonesia --periode 2022-2025

# Tambahkan data pesaing dari CSV milik Anda
python src/app.py --produk "sepatu olahraga" --pesaing data/pesaing_saya.csv
```

| Argumen | Keterangan | Default |
|---|---|---|
| `--produk` | Kata kunci produk (wajib) | – |
| `--lokasi` | `Indonesia`, `Malaysia`, `Singapura`, `Global`, atau kode ISO negara | `Indonesia` |
| `--periode` | Rentang tahun `YYYY-YYYY` | `2022-2025` |
| `--pesaing` | Path CSV pesaing | – |
| `--output` | Folder hasil | `output/` |
| `--demo` | Pakai data contoh offline | – |

### Format CSV pesaing

Kolom wajib `nama` dan `harga` (angka, Rupiah). Kolom opsional `rating` dan `terjual`.

```csv
nama,harga,rating,terjual
Brand A Runner,500000,4.8,12000
Brand B Pro,450000,4.7,9500
```

Data pesaing sengaja diambil dari CSV, bukan scraping otomatis: scraping marketplace sering melanggar ketentuan layanan dan mudah rusak saat tampilan situs berubah. Anda bisa mengisi CSV secara manual atau dari ekspor resmi platform.

### Contoh output (mode demo)

```
=== Ringkasan Riset Pasar 'sepatu olahraga' ===
- Tren Permintaan: naik +29.9% (puncak 2025-04)
- Wilayah teratas: DKI Jakarta, Jawa Barat, Banten
- Top Pesaing: Brand D Lite (Rp320.000), Brand A Runner (Rp500.000), Brand B Pro (Rp450.000)
- Range Harga Pasar: Rp320.000–Rp600.000
Laporan, grafik, dan CSV disimpan di 'output/sepatu-olahraga'.
```

> Angka di atas berasal dari data contoh (dummy), bukan data pasar nyata.

## Struktur Folder

```
alat-riset-pasar/
├─ src/
│  ├─ app.py            # Entrypoint CLI
│  ├─ analysis.py       # Pengambilan data dan analisis
│  └─ visualization.py  # Grafik dan laporan
├─ data/                # Data contoh untuk mode demo
├─ tests/               # Pytest
├─ output/              # Hasil riset (diabaikan git)
└─ .github/workflows/   # CI
```

## Cara Kerja Analisis

- **Arah tren**: rata-rata minat 3 bulan pertama dibandingkan 3 bulan terakhir. Perubahan di atas +5% = naik, di bawah −5% = turun, selain itu stabil.
- **Indeks minat** Google Trends bersifat relatif (0–100), bukan volume pencarian absolut.
- Google Trends membatasi frekuensi permintaan; jika muncul error 429, tunggu beberapa menit lalu coba lagi.

## Privasi

Alat ini hanya memproses data agregat publik (Google Trends) dan CSV yang Anda berikan. Tidak ada data pribadi yang dikumpulkan atau dikirim ke mana pun.

## Pengembangan

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Roadmap

- [ ] Ekspor laporan ke HTML/PDF
- [ ] Antarmuka web (Flask) dengan grafik interaktif
- [ ] Bandingkan beberapa kata kunci sekaligus
- [ ] Modul Deep Research opsional untuk sintesis multisumber

## Lisensi

[MIT](LICENSE)
