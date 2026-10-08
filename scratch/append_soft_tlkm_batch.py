import json

def make_md_cell(cell_id, text):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

def make_code_cell(cell_id, text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

with open('notebooks/09_barang_consolidation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# -----------------------------------------------------------------------------
# Section 69: SOFT-ENG
# -----------------------------------------------------------------------------
s69_md = make_md_cell("cell_s69_md", """---
## 69. Subcategory SOFT-ENG Consolidation & Standardization
### Engineering Software Normalization & Brand Alignment

- Separates software titles cleanly by brand, name, version year, and license count.
- Standardizes all product titles into clean Title Case without brand repetition (`AutoCAD LT 2006`, `Tekla Structures 12`, `ETAP`, `STAAD.Pro 2007`, `CAESAR II 450`, `PDMS 11.6`, `Primavera`, `AutoCAD Architecture 2009`, `AutoCAD Mechanical 2009`, `AutoCAD Electrical 2009`, `Inventor 2009`, `Revit 2009`, `MicroStation V8i`, `Navisworks Manage 2010`, `AFES`, `AutoCAD 2013`, `E-Tank`, `Solid Edge`, `HAP HVAC`, `CAESAR II`, `COMPRESS`, `InstruCalc 8.1`, `SmartSketch`, `SketchUp & V-Ray`, `Lumion Pro`).
- Corrects brand assignment for `AutoCAD 2013` from legacy hardware bundle (Lenovo) to Autodesk (`brand_id: 23`).
- Corrects typos: `INSTRUCAL` -> `InstruCalc`, `Smart Sketch` -> `SmartSketch`.
- Preserves all 26 master barangs across 31 units (100% units preserved).
""")

s69_code = make_code_cell("cell_s69_code", """# =============================================================================
# 69. SOFT-ENG Consolidation & Standardization
# =============================================================================
print("\\n" + "=" * 80)
print("Consolidating SOFT-ENG")
print("=" * 80 + "\\n")

SUB_ENG = 'SOFT-ENG'
df_eng_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_ENG}.csv', dtype=str)

TARGET_ENG = [
    ('23', 'AutoCAD LT 2006', '2D CAD Drafting', [3009]),
    ('28', 'Tekla Structures 12', '1 Lisensi, Software Drawing Civil', [3022]),
    ('32', 'ETAP', 'Software Analisis Elektrikal', [3034]),
    ('33', 'STAAD.Pro 2007', 'Software Analisis Struktur Civil', [3053]),
    ('60', 'CAESAR II 450', 'Piping Stress Analysis', [3072]),
    ('36', 'PDMS 11.6', 'Software Desain 3D Plant', [3119]),
    ('37', 'Primavera', 'Project Management', [3128]),
    ('23', 'AutoCAD Architecture 2009', 'Desain Arsitektur', [3144, 3145, 3146, 3147]),
    ('23', 'AutoCAD Mechanical 2009', 'Desain Mekanikal', [3148, 3149, 3150]),
    ('23', 'AutoCAD Electrical 2009', 'Desain Elektrikal', [3151]),
    ('23', 'Inventor 2009', 'Desain Mekanikal 3D', [3152]),
    ('23', 'Revit 2009', 'BIM & Desain Bangunan', [3153]),
    ('33', 'MicroStation V8i', 'Software CAD 2D & 3D', [3164]),
    ('23', 'Navisworks Manage 2010', 'Review & Koordinasi Desain 3D', [3206]),
    ('42', 'AFES', 'Perhitungan Pondasi Civil', [3229]),
    ('23', 'AutoCAD 2013', 'Network License - 15 Lisensi', [3592]),
    ('46', 'E-Tank', 'Mobile User - 2 Lisensi, Perhitungan Tangki', [3595]),
    ('58', 'Solid Edge', '3 Lisensi, Desain 3D CAD', [3786]),
    ('59', 'HAP HVAC', 'Hourly Analysis Program HVAC', [3787]),
    ('60', 'CAESAR II', 'Pipe Stress Analysis - 1 Lisensi', [3788]),
    ('61', 'COMPRESS', 'Bejana Tekan, ASME License', [3793]),
    ('62', 'InstruCalc 8.1', 'Desain Instrumentasi', [3794]),
    ('60', 'CAESAR II', 'Pipe Stress Analysis - 2 Lisensi', [3806]),
    ('60', 'SmartSketch', 'Desain CAD 2D', [3835]),
    ('68', 'SketchUp & V-Ray', 'Modeling 3D & Rendering', [3991]),
    ('69', 'Lumion Pro', 'Software Rendering Arsitektur 3D', [3992])
]

sub_barangs_eng = []
sub_lots_eng = []
eng_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_ENG, start=1):
    barang_num = f'{SUB_ENG}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_ENG],
        'brand_id': b_id, 'uom_id': 1, 'name': name_val, 'specification': spec_val,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    }
    l_dict = {
        'id': seq_counter, 'number': lot_num, 'barang_id': seq_counter,
        'organizer_id': 1, 'vendor_id': None, 'legacy_vendor_id': None,
        'location_id': None, 'initial_quantity': None, 'current_quantity': None,
        'po_number': None, 'date_of_receipt': now_str, 'unit_price': None,
        'image_url': None, 'burden': None, 'project_id': None,
        'created_at': now_str, 'updated_at': now_str
    }
    sub_barangs_eng.append(b_dict)
    sub_lots_eng.append(l_dict)
    for aid in aids:
        eng_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_eng).to_csv(STAGING_BARANGS_DIR / f'{SUB_ENG}.csv', index=False)
pd.DataFrame(sub_lots_eng).to_csv(STAGING_LOTS_DIR / f'{SUB_ENG}.csv', index=False)

for idx in df_eng_units.index:
    aid = str(df_eng_units.at[idx, 'ams_asset_id']).strip()
    if aid in eng_unit_lot_map:
        lot_id, spec = eng_unit_lot_map[aid]
        df_eng_units.at[idx, 'lot_id'] = lot_id
        df_eng_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_eng_units.columns:
        df_eng_units[c] = pd.to_numeric(df_eng_units[c], errors='coerce').astype('Int64')
df_eng_units.to_csv(STAGING_UNITS_DIR / f'{SUB_ENG}.csv', index=False)

sync_consolidated_masters()

assert len(sub_barangs_eng) == 26, f'Expected 26 barangs in SOFT-ENG, got {len(sub_barangs_eng)}'
assert len(df_eng_units) == 31, f'Expected 31 units in SOFT-ENG, got {len(df_eng_units)}'
print("[SUCCESS] SOFT-ENG successfully standardized and verified.")
""")

# -----------------------------------------------------------------------------
# Section 70: SOFT-GEN
# -----------------------------------------------------------------------------
s70_md = make_md_cell("cell_s70_md", """---
## 70. Subcategory SOFT-GEN Consolidation & Standardization
### General Software Normalization & Typo Resolution

- Resolves generic names (`OPERATING SYSTEM`, `OFFICE SOFT`) into exact operating systems, office applications, and utilities.
- Fixes typos: `MICORSOFT` -> `Microsoft`, `ACCEST` -> `Access`.
- Standardizes product editions: `Windows XP Professional`, `Windows Vista Business`, `Windows 8 Pro`, `Windows 8.1 Professional`, `Windows Server 2008 R2`, `Windows Server 2012 Standard`, `Office 2003 Standard`, `Office 2007 Standard`, `Office 2010 Standard`, `Office 2013 Standard`, `Excel 2007`, `Access 2007`, `Project 2007`, `Project 2010`, `SQL Server 2012 Standard`, `Windows Server CAL`, `SQL Server CAL`, `Kaspersky Endpoint Security`, `Kaspersky Anti-Virus v6`, `Kaspersky BusinessSpace Security v6`, `Acrobat Pro`, `Acrobat Pro 2013`, `Neo Accounting`.
- Preserves all 24 master barangs across 25 units (100% units preserved).
""")

s70_code = make_code_cell("cell_s70_code", """# =============================================================================
# 70. SOFT-GEN Consolidation & Standardization
# =============================================================================
print("\\n" + "=" * 80)
print("Consolidating SOFT-GEN")
print("=" * 80 + "\\n")

SUB_GEN = 'SOFT-GEN'
df_gen_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_GEN}.csv', dtype=str)

TARGET_GEN = [
    ('10', 'Neo Accounting', 'Software Akuntansi', [2635]),
    ('22', 'Windows XP Professional', 'Sistem Operasi', [3007]),
    ('22', 'Office 2003 Standard', 'Aplikasi Perkantoran', [3008]),
    ('34', 'Acrobat Pro', 'PDF Editor & Creator', [3073]),
    ('35', 'Kaspersky Endpoint Security', 'Antivirus Corporate', [3074]),
    ('22', 'Project 2007', 'Project Management', [3075]),
    ('22', 'Windows Server 2008 R2', 'Sistem Operasi Server', [3154]),
    ('35', 'Kaspersky Anti-Virus v6', 'Antivirus Client', [3155]),
    ('22', 'Windows Vista Business', 'Sistem Operasi', [3156]),
    ('22', 'Excel 2007', 'Spreadsheet', [3157]),
    ('22', 'Access 2007', 'Database Management', [3158]),
    ('22', 'Office 2007 Standard', 'Aplikasi Perkantoran', [3165]),
    ('35', 'Kaspersky BusinessSpace Security v6', '210 Lisensi', [3590]),
    ('22', 'Windows 8 Pro', 'Sistem Operasi', [3591]),
    ('22', 'Office 2010 Standard', '20 Lisensi', [3593]),
    ('22', 'Project 2010', '5 Lisensi', [3594]),
    ('22', 'Windows Server 2012 Standard', '3 Lisensi', [3789]),
    ('22', 'SQL Server 2012 Standard', '1 Lisensi', [3790]),
    ('22', 'Windows Server CAL', '100 Lisensi', [3791]),
    ('22', 'SQL Server CAL', '10 Lisensi', [3792]),
    ('35', 'Kaspersky BusinessSpace Security v6', '300 Lisensi (2013-2014)', [3795, 3797]),
    ('34', 'Acrobat Pro 2013', '10 Lisensi', [3796]),
    ('22', 'Windows 8.1 Professional', '100 Lisensi OLP', [3798]),
    ('22', 'Office 2013 Standard', '25 Lisensi OLP', [3799])
]

sub_barangs_gen = []
sub_lots_gen = []
gen_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_GEN, start=1):
    barang_num = f'{SUB_GEN}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_GEN],
        'brand_id': b_id, 'uom_id': 1, 'name': name_val, 'specification': spec_val,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    }
    l_dict = {
        'id': seq_counter, 'number': lot_num, 'barang_id': seq_counter,
        'organizer_id': 1, 'vendor_id': None, 'legacy_vendor_id': None,
        'location_id': None, 'initial_quantity': None, 'current_quantity': None,
        'po_number': None, 'date_of_receipt': now_str, 'unit_price': None,
        'image_url': None, 'burden': None, 'project_id': None,
        'created_at': now_str, 'updated_at': now_str
    }
    sub_barangs_gen.append(b_dict)
    sub_lots_gen.append(l_dict)
    for aid in aids:
        gen_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_gen).to_csv(STAGING_BARANGS_DIR / f'{SUB_GEN}.csv', index=False)
pd.DataFrame(sub_lots_gen).to_csv(STAGING_LOTS_DIR / f'{SUB_GEN}.csv', index=False)

for idx in df_gen_units.index:
    aid = str(df_gen_units.at[idx, 'ams_asset_id']).strip()
    if aid in gen_unit_lot_map:
        lot_id, spec = gen_unit_lot_map[aid]
        df_gen_units.at[idx, 'lot_id'] = lot_id
        df_gen_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_gen_units.columns:
        df_gen_units[c] = pd.to_numeric(df_gen_units[c], errors='coerce').astype('Int64')
df_gen_units.to_csv(STAGING_UNITS_DIR / f'{SUB_GEN}.csv', index=False)

sync_consolidated_masters()

assert len(sub_barangs_gen) == 24, f'Expected 24 barangs in SOFT-GEN, got {len(sub_barangs_gen)}'
assert len(df_gen_units) == 25, f'Expected 25 units in SOFT-GEN, got {len(df_gen_units)}'
print("[SUCCESS] SOFT-GEN successfully standardized and verified.")
""")

# -----------------------------------------------------------------------------
# Section 71: TLKM-FAX & TLKM-SP
# -----------------------------------------------------------------------------
s71_md = make_md_cell("cell_s71_md", """---
## 71. Subcategories TLKM-FAX & TLKM-SP Standardization & Polish
### Fax Machine & Specialized Equipment Polish

- `TLKM-FAX`: Title Cases fax items and removes redundant brand prefixes (`Mesin Fax 14.4 kbps`, `Mesin Fax 33.6 kbps`). Preserves all 2 barangs across 2 units.
- `TLKM-SP`: Title Cases intrinsically safe camera specification (`Intrinsically Safe Camera Smart-Ex 03 DZ1`). Preserves 1 barang across 1 unit.
""")

s71_code = make_code_cell("cell_s71_code", """# =============================================================================
# 71. TLKM-FAX & TLKM-SP Standardization & Polish
# =============================================================================
print("\\n" + "=" * 80)
print("Standardizing TLKM-FAX & TLKM-SP")
print("=" * 80 + "\\n")

# 1. TLKM-FAX
SUB_FAX = 'TLKM-FAX'
df_fax_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_FAX}.csv', dtype=str)

TARGET_FAX = [
    ('25', 'Mesin Fax 14.4 kbps', '14.4 kbps', [2645]),
    ('17', 'Mesin Fax 33.6 kbps', '33.6 kbps', [3015])
]

sub_barangs_fax = []
sub_lots_fax = []
fax_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_FAX, start=1):
    barang_num = f'{SUB_FAX}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_FAX],
        'brand_id': b_id, 'uom_id': 1, 'name': name_val, 'specification': spec_val,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    }
    l_dict = {
        'id': seq_counter, 'number': lot_num, 'barang_id': seq_counter,
        'organizer_id': 1, 'vendor_id': None, 'legacy_vendor_id': None,
        'location_id': None, 'initial_quantity': None, 'current_quantity': None,
        'po_number': None, 'date_of_receipt': now_str, 'unit_price': None,
        'image_url': None, 'burden': None, 'project_id': None,
        'created_at': now_str, 'updated_at': now_str
    }
    sub_barangs_fax.append(b_dict)
    sub_lots_fax.append(l_dict)
    for aid in aids:
        fax_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_fax).to_csv(STAGING_BARANGS_DIR / f'{SUB_FAX}.csv', index=False)
pd.DataFrame(sub_lots_fax).to_csv(STAGING_LOTS_DIR / f'{SUB_FAX}.csv', index=False)

for idx in df_fax_units.index:
    aid = str(df_fax_units.at[idx, 'ams_asset_id']).strip()
    if aid in fax_unit_lot_map:
        lot_id, spec = fax_unit_lot_map[aid]
        df_fax_units.at[idx, 'lot_id'] = lot_id
        df_fax_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_fax_units.columns:
        df_fax_units[c] = pd.to_numeric(df_fax_units[c], errors='coerce').astype('Int64')
df_fax_units.to_csv(STAGING_UNITS_DIR / f'{SUB_FAX}.csv', index=False)

# 2. TLKM-SP
SUB_SP = 'TLKM-SP'
df_sp_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_SP}.csv', dtype=str)

TARGET_SP = [
    ('149', 'Kamera Hazardous', 'Intrinsically Safe Camera Smart-Ex 03 DZ1', [11846])
]

sub_barangs_sp = []
sub_lots_sp = []
sp_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_SP, start=1):
    barang_num = f'{SUB_SP}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_SP],
        'brand_id': b_id, 'uom_id': 1, 'name': name_val, 'specification': spec_val,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    }
    l_dict = {
        'id': seq_counter, 'number': lot_num, 'barang_id': seq_counter,
        'organizer_id': 1, 'vendor_id': None, 'legacy_vendor_id': None,
        'location_id': None, 'initial_quantity': None, 'current_quantity': None,
        'po_number': None, 'date_of_receipt': now_str, 'unit_price': None,
        'image_url': None, 'burden': None, 'project_id': None,
        'created_at': now_str, 'updated_at': now_str
    }
    sub_barangs_sp.append(b_dict)
    sub_lots_sp.append(l_dict)
    for aid in aids:
        sp_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_sp).to_csv(STAGING_BARANGS_DIR / f'{SUB_SP}.csv', index=False)
pd.DataFrame(sub_lots_sp).to_csv(STAGING_LOTS_DIR / f'{SUB_SP}.csv', index=False)

for idx in df_sp_units.index:
    aid = str(df_sp_units.at[idx, 'ams_asset_id']).strip()
    if aid in sp_unit_lot_map:
        lot_id, spec = sp_unit_lot_map[aid]
        df_sp_units.at[idx, 'lot_id'] = lot_id
        df_sp_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_sp_units.columns:
        df_sp_units[c] = pd.to_numeric(df_sp_units[c], errors='coerce').astype('Int64')
df_sp_units.to_csv(STAGING_UNITS_DIR / f'{SUB_SP}.csv', index=False)

sync_consolidated_masters()

assert len(sub_barangs_fax) == 2, f'Expected 2 barangs in TLKM-FAX, got {len(sub_barangs_fax)}'
assert len(df_fax_units) == 2, f'Expected 2 units in TLKM-FAX, got {len(df_fax_units)}'
assert len(sub_barangs_sp) == 1, f'Expected 1 barang in TLKM-SP, got {len(sub_barangs_sp)}'
assert len(df_sp_units) == 1, f'Expected 1 unit in TLKM-SP, got {len(df_sp_units)}'
print("[SUCCESS] TLKM-FAX and TLKM-SP successfully standardized and verified.")
""")

# -----------------------------------------------------------------------------
# Section 72: TLKM-TL
# -----------------------------------------------------------------------------
s72_md = make_md_cell("cell_s72_md", """---
## 72. Subcategory TLKM-TL Consolidation & Duplicate Merge
### Telephone Duplicate Merge & Final Clean

- Consolidates from 6 down to **4 master barangs** across all 115 units (Net -2 barangs):
  - `TLKM-TL-0001`: `Pesawat Telepon` (Spec: `Warna Putih`, Brand: Panasonic [25]) across 4 units.
  - `TLKM-TL-0002`: `Pesawat Telepon` (Spec: `Warna Hitam`, Brand: Panasonic [25]) across 7 units.
  - `TLKM-TL-0003`: `Pesawat Telepon` (Spec: `NULL`, Brand: Panasonic [25]) across 103 units (merged `0003`, `0005`, and `0006`).
  - `TLKM-TL-0004`: `Pesawat Telepon` (Spec: `NULL`, Brand: Sahitel [79]) across 1 unit.
- Preserves all 115 units (100% units preserved).
""")

s72_code = make_code_cell("cell_s72_code", """# =============================================================================
# 72. TLKM-TL Consolidation & Duplicate Merge
# =============================================================================
print("\\n" + "=" * 80)
print("Consolidating TLKM-TL")
print("=" * 80 + "\\n")

SUB_TL = 'TLKM-TL'
df_tl_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_TL}.csv', dtype=str)

aids_white = [97, 266, 306, 326]
aids_black = [305, 668, 669, 670, 671, 1077, 1078]
aids_sahitel = [907]
all_aids = df_tl_units['ams_asset_id'].astype(int).tolist()
merged_aids = [a for a in all_aids if a not in aids_white and a not in aids_black and a not in aids_sahitel]

TARGET_TL = [
    ('25', 'Pesawat Telepon', 'Warna Putih', aids_white),
    ('25', 'Pesawat Telepon', 'Warna Hitam', aids_black),
    ('25', 'Pesawat Telepon', None, merged_aids),
    ('79', 'Pesawat Telepon', None, aids_sahitel)
]

sub_barangs_tl = []
sub_lots_tl = []
tl_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_TL, start=1):
    barang_num = f'{SUB_TL}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_TL],
        'brand_id': b_id, 'uom_id': 1, 'name': name_val, 'specification': spec_val,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    }
    l_dict = {
        'id': seq_counter, 'number': lot_num, 'barang_id': seq_counter,
        'organizer_id': 1, 'vendor_id': None, 'legacy_vendor_id': None,
        'location_id': None, 'initial_quantity': None, 'current_quantity': None,
        'po_number': None, 'date_of_receipt': now_str, 'unit_price': None,
        'image_url': None, 'burden': None, 'project_id': None,
        'created_at': now_str, 'updated_at': now_str
    }
    sub_barangs_tl.append(b_dict)
    sub_lots_tl.append(l_dict)
    for aid in aids:
        tl_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_tl).to_csv(STAGING_BARANGS_DIR / f'{SUB_TL}.csv', index=False)
pd.DataFrame(sub_lots_tl).to_csv(STAGING_LOTS_DIR / f'{SUB_TL}.csv', index=False)

for idx in df_tl_units.index:
    aid = str(df_tl_units.at[idx, 'ams_asset_id']).strip()
    if aid in tl_unit_lot_map:
        lot_id, spec = tl_unit_lot_map[aid]
        df_tl_units.at[idx, 'lot_id'] = lot_id
        df_tl_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_tl_units.columns:
        df_tl_units[c] = pd.to_numeric(df_tl_units[c], errors='coerce').astype('Int64')
df_tl_units.to_csv(STAGING_UNITS_DIR / f'{SUB_TL}.csv', index=False)

sync_consolidated_masters()

assert len(sub_barangs_tl) == 4, f'Expected 4 barangs in TLKM-TL, got {len(sub_barangs_tl)}'
assert len(df_tl_units) == 115, f'Expected 115 units in TLKM-TL, got {len(df_tl_units)}'
print("[SUCCESS] TLKM-TL successfully consolidated and verified.")
""")

# -----------------------------------------------------------------------------
# Section 73: Final End-to-End Migration Quality Assertions & Complete Audit
# -----------------------------------------------------------------------------
s73_md = make_md_cell("cell_s73_md", """---
## 73. Final End-to-End Migration Quality Assertions & Complete Subcategory Audit
### 100% Inventory Consolidation Milestone

- Final validation covering **all 110 subcategories** across the entire AMS-to-SMART data migration.
- System-wide invariant checks: exactly **665 master barangs**, **665 master lots**, and **6,939 master units** (100% preserved).
- Complete foreign key integrity verification between units and lots.
- Monotonic sequence verification: IDs `1..665` without any gaps or duplicates.
""")

s73_code = make_code_cell("cell_s73_code", """# =============================================================================
# 73. Final End-to-End Migration Quality Assertions & Complete Subcategory Audit
# =============================================================================
print("\\n" + "=" * 80)
print("FINAL END-TO-END MIGRATION QUALITY ASSERTIONS & AUDIT (ALL 110 SUBCATEGORIES)")
print("=" * 80 + "\\n")

# 1. Batch unit checks
final_batch_units = {
    'SOFT-ENG': 31,
    'SOFT-GEN': 25,
    'TLKM-FAX': 2,
    'TLKM-SP': 1,
    'TLKM-TL': 115
}

for sub_c, exp_count in final_batch_units.items():
    df_u_part = pd.read_csv(STAGING_UNITS_DIR / f'{sub_c}.csv')
    df_b_part = pd.read_csv(STAGING_BARANGS_DIR / f'{sub_c}.csv')
    df_l_part = pd.read_csv(STAGING_LOTS_DIR / f'{sub_c}.csv')
    assert len(df_u_part) == exp_count, f"Mismatch in {sub_c}: expected {exp_count} units, got {len(df_u_part)}"
    assert len(df_b_part) == len(df_l_part), f"Barangs vs Lots mismatch in {sub_c}: {len(df_b_part)} vs {len(df_l_part)}"
    assert df_u_part['lot_id'].isin(df_l_part['id']).all(), f"Invalid lot_id found in {sub_c} units!"

# 2. Complete 110 Subcategories Audit
with open(STAGING_BARANGS_DIR / '_barangs_manifest.json') as f:
    b_manifest = json.load(f)

assert len(b_manifest['subcategories']) == 110, f"Expected 110 subcategories, got {len(b_manifest['subcategories'])}"

for sub_code, meta in b_manifest['subcategories'].items():
    p_b = STAGING_BARANGS_DIR / meta['file']
    p_l = STAGING_LOTS_DIR / meta['file']
    p_u = STAGING_UNITS_DIR / meta['file']
    assert p_b.exists(), f"Missing staging barang file for {sub_code}"
    assert p_l.exists(), f"Missing staging lot file for {sub_code}"
    assert p_u.exists(), f"Missing staging unit file for {sub_code}"
    df_b = pd.read_csv(p_b)
    df_l = pd.read_csv(p_l)
    df_u = pd.read_csv(p_u)
    assert len(df_b) == len(df_l), f"Barangs vs lots count mismatch in {sub_code}: {len(df_b)} vs {len(df_l)}"
    assert df_u['lot_id'].isin(df_l['id']).all(), f"Invalid foreign key lot_id in {sub_code} units"

# 3. Global Master Tables Final Assertions
df_barangs_m = pd.read_csv(FINAL_BARANG_DIR / 'barangs.csv')
df_lots_m = pd.read_csv(FINAL_LOT_DIR / 'lots.csv')
df_units_m = pd.read_csv(FINAL_UNIT_DIR / 'units.csv')

assert len(df_barangs_m) == 665, f"Expected 665 barangs, got {len(df_barangs_m)}"
assert len(df_lots_m) == 665, f"Expected 665 lots, got {len(df_lots_m)}"
assert len(df_units_m) == 6939, f"Expected 6,939 units, got {len(df_units_m)}"

assert (df_barangs_m['id'].astype(int) == list(range(1, 666))).all(), "Barang IDs are not strictly 1..665"
assert (df_lots_m['id'].astype(int) == list(range(1, 666))).all(), "Lot IDs are not strictly 1..665"
assert (df_lots_m['barang_id'].astype(int) == list(range(1, 666))).all(), "Lot barang_id foreign keys are not strictly 1..665"
assert df_barangs_m['number'].is_unique, "Barang numbers are not unique"
assert df_lots_m['number'].is_unique, "Lot numbers are not unique"
assert df_units_m['lot_id'].isin(df_lots_m['id']).all(), "Orphan lot_id found in final units!"

# Status distribution verification
status_counts = df_units_m['status'].value_counts().to_dict()
assert status_counts == {'Tersedia': 5159, 'Borrowed': 1282, 'Tidak Aktif': 498}, f"Unexpected status counts: {status_counts}"

print("=" * 80)
print("[SUCCESS] ALL 110 SUBCATEGORIES FULLY CONSOLIDATED & VALIDATED WITH 100% INTEGRITY!")
print(f"Master Barangs: {len(df_barangs_m):,} (reduced from 888 legacy barangs down to 665)")
print(f"Master Lots:    {len(df_lots_m):,} (reduced from 888 legacy lots down to 665)")
print(f"Master Units:   {len(df_units_m):,} (100% preserved, 0 units lost)")
print(f"Status Counts:  {status_counts}")
print("=" * 80)
""")

new_cells = [
    s69_md, s69_code,
    s70_md, s70_code,
    s71_md, s71_code,
    s72_md, s72_code,
    s73_md, s73_code
]

for i, c in enumerate(new_cells):
    if c['cell_type'] == 'code':
        src = "".join(c['source'])
        compile(src, f'<new_cell_{i}>', 'exec')
print("All new cells compiled with ZERO syntax errors.")

nb['cells'].extend(new_cells)

with open('notebooks/09_barang_consolidation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Appended 10 new cells (Sections 69 through 73). Total notebook cells: {len(nb['cells'])}.")
