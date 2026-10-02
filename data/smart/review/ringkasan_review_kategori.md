# Ringkasan Eksekutif & Panduan Tinjauan Master Data (Kategori & Subkategori)
### Migrasi Data Legacy AMS ke Microsoft SQL Server Smart
**Tanggal Dokumen:** 01 October 2026  
**Target Pembaca:** Tim Manajemen Aset & Tim IT  
**File Excel Review Utama:** [`Review_Master_Kategori_dan_Subkategori.xlsx`](Review_Master_Kategori_dan_Subkategori.xlsx)

---

## 1. Urgensi & Latar Belakang
Master data Kategori dan Subkategori merupakan fondasi relasional utama dalam sistem manajemen aset. Sebelum proses pembersihan ribuan unit aset fisik dijalankan, struktur master data harus disepakati dan memperoleh **persetujuan (approval)** dari Tim Pengelola Aset dan Tim IT.

Dokumen ini dan file Excel terlampir disusun untuk memudahkan kedua tim dalam melakukan review, memberikan masukan, dan menandatangani persetujuan secara formal.

---

## 2. Ringkasan Transformasi Data (AMS Legacy vs Smart)

| Indikator Transformasi | Kondisi AMS Legacy | Hasil Standar Smart | Catatan Transformasi |
|:---|:---:|:---:|:---|
| **Kategori Induk** | 15 Baris (`control='F'`) | **13 Kategori Aktif** | Penggabungan kategori duplikat (`PROP` & `KEND`), eksklusi kategori nonaktif (`PUR`). |
| **Subkategori** | 113 Baris (`control='T'`) | **110 Subkategori Standar** | Deduplikasi `LIFT` & `MOBIL`, penamaan terstandar `<INDUK>-<ANAK>`. |
| **Subkategori Yatim (Orphan)** | 24 Item (`parent = NULL`) | **0 Subkategori Yatim** | 24 item dihubungkan kembali ke kategori induk sesuai prefiks kode legacy. |
| **Kategori Baru Mandiri** | Belum terpisah | **1 Kategori (`TLKM`)** | Perangkat telekomunikasi (Telepon, Smartphone, HT, Fax) dipisah dari Aksesoris/Elektronik. |
| **Resolusi Bentrok Kode & Reklasifikasi** | 1 Bentrok (`WH`) | **Terselesaikan** | `ACC-WB` (Whiteboard tetap di Aksesoris) & `MES-WTH` (Water Heater dipindah ke Mesin). |

---

## 3. Daftar Master Kategori Smart (13 Kategori)

| ID | Kode | Nama Kategori | Kode AMS Asal | Subkategori | Deskripsi / Cakupan Operasional |
|:--:|:----:|:--------------|:-------------:|:-----------:|:--------------------------------|
| 1 | `FUR` | Furniture | 100000 | 8 | Perabotan kantor (kursi, meja, lemari, rak, sofa). |
| 2 | `ACC` | Aksesoris | 110000 | 40 | Aksesoris & fixture kantor (whiteboard, jam dinding, bracket, brankas). |
| 3 | `COMP` | Computer | 120000 | 4 | Komputer desktop, notebook, workstation, server IT. |
| 4 | `MON` | Monitor | 130000 | 2 | Monitor komputer (tabung, LCD/LED display). |
| 5 | `PERP` | Peripheral | 140000 | 14 | Perangkat periferal, storage eksternal, multimedia, networking. |
| 6 | `PRNT` | Printer | 150000 | 6 | Printer inkjet, laserjet, plotter, ID card printer. |
| 7 | `SOFT` | Software | 160000 | 2 | Lisensi perangkat lunak engineering dan aplikasi perkantoran. |
| 8 | `PROP` | Properti & Gedung | 170000, 220000 | 1 | Konsolidasi properti tanah dan bangunan gedung. |
| 9 | `MES` | Mesin | 180000 | 5 | Mesin dan utilitas gedung (water heater, genset, lift, panel listrik, pompa air). |
| 10 | `KEND` | Kendaraan | 200000, 250000 | 1 | Konsolidasi kendaraan dinas/operasional dan otomotif. |
| 11 | `ELEK` | Elektronik | 240000 | 18 | Peralatan elektronik umum, keamanan gedung, sensor, sound system (CCTV, TV). |
| 12 | `PDGR` | Pendingin Ruangan | 260000 | 5 | Sistem tata udara dan pendingin ruangan (AC Split, AC Portable, AHU). |
| 13 | `TLKM` | Telekomunikasi | 110004, 140007, 240013, 240015, 110030 | 4 | Kategori mandiri baru untuk perangkat telekomunikasi (Telepon, Smartphone, HT, Fax). |

---

## 4. Keputusan Penting Pembersihan Data (Changelog & Rationale)

1. **Konsolidasi Properti & Gedung (`PROP`)**:
   - *Kondisi Lama*: Terpisah menjadi `170000 PROPERTI` dan `220000 GEDUNG`.
   - *Keputusan*: Digabung menjadi **`PROP` (Properti & Gedung)** karena perlakuan aset dan amortisasi tanah/bangunan terpadu.
2. **Konsolidasi Kendaraan & Otomotif (`KEND`)**:
   - *Kondisi Lama*: Terpisah menjadi `200000 KENDARAAN` dan `250000 OTOMOTIF`.
   - *Keputusan*: Digabung menjadi **`KEND` (Kendaraan)** untuk menghilangkan kerancuan pengelompokan kendaraan.
3. **Pembentukan Kategori Telekomunikasi (`TLKM`)**:
   - *Kondisi Lama*: Tersebar di bawah Aksesoris, Peripheral, dan Elektronik.
   - *Keputusan*: Dibentuk kategori khusus **`TLKM`** agar tata kelola perangkat komunikasi kantor terstandar.
4. **Reklasifikasi Water Heater & Resolusi Bentrok Kode**:
   - *Kondisi Lama*: `Whiteboard` dan `Water Heater` berada di bawah Aksesoris (`ACC`) dan sama-sama memakai kode `WH`.
   - *Keputusan*: `Water Heater` dipindahkan ke kategori **Mesin (`MES`)** sebagai **`MES-WTH`** (karena merupakan peralatan utilitas mekanikal gedung), sedangkan `Whiteboard` tetap di **Aksesoris (`ACC`)** sebagai **`ACC-WB`**.
5. **Deduplikasi `LIFT`**:
   - *Kondisi Lama*: Muncul ganda di Mesin (`180005`, `LIF`) dan Elektronik (`240017`, `LT`).
   - *Keputusan*: Digabung menjadi **`MES-LIF`**. Kedua kode lama tetap dipetakan ke target yang sama di tabel lookup.
6. **Deduplikasi `MOBIL`**:
   - *Kondisi Lama*: Tercatat ganda sebagai `200001` (Kendaraan Operasional RE) dan `200002` (Mobil).
   - *Keputusan*: Dikonsolidasi ke **`KEND-MO`** (`Mobil`).
7. **Penautan Kembali 24 Subkategori Yatim**:
   - *Kondisi Lama*: 24 item berstatus subkategori (`control='T'`) memiliki `parent = NULL`.
   - *Keputusan*: Dipetakan ulang ke induk aslinya (`PDGR`, `MES`, `ELEK`) berdasarkan prefiks angka kodenya.
8. **Eksklusi Kategori Tidak Aktif (`210000 PURNAMA`)**:
   - *Kondisi Lama*: Tercatat di AMS dengan 0 subkategori.
   - *Keputusan*: Dikecualikan dari master aktif Smart, namun tetap diaudit di staging.

---

## 5. Panduan Pengisian Lembar Kerja Excel
Stakeholder diharapkan membuka file **`Review_Master_Kategori_dan_Subkategori.xlsx`**:
1. Masuk ke sheet **`Master_Kategori`** dan **`Master_Subkategori`**.
2. Isikan kolom **`Status Persetujuan`** (pilih melalui dropdown: *Disetujui*, *Perlu Penyesuaian*, atau *Ditolak*).
3. Apabila ada masukan atau kebutuhan perubahan nama/kategori, tuliskan pada kolom **`Catatan & Masukan Tim Aset & IT`**.
4. File yang telah diisi dapat dikembalikan kepada tim data migration untuk difinalisasi.
