import json
import uuid

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
# Section 64: PERP-UPS & PERP-VGA
# -----------------------------------------------------------------------------
s64_md = make_md_cell("cell_s64_md", """---
## 64. Subcategories PERP-UPS & PERP-VGA Consolidation
### UPS Brand Alignment & VGA Normalization

- `PERP-UPS`: Standardizes names and capacity specifications into Title Case, strips brand repetition from names (`UPS 10 kVA`, `UPS 6000 VA`, `UPS SIN 3100`), and corrects `PERP-UPS-0004` (Asset 6520, APC Smart-UPS 5000) from legacy brand ICA (174) to APC (86). Preserves all 4 barangs across 6 units.
- `PERP-VGA`: Strips legacy category ID prefix `140016` from `140016 Geforce GTX980` to clean `GeForce GTX 980` (4 GB), Title Cases `Quadro FX 580` (512 MB). Preserves all 2 barangs across 3 units.
""")

s64_code = make_code_cell("cell_s64_code", """# =============================================================================
# 64. PERP-UPS & PERP-VGA Consolidation
# =============================================================================
print("\\n" + "=" * 80)
print("Consolidating PERP-UPS & PERP-VGA")
print("=" * 80 + "\\n")

# 1. PERP-UPS
SUB_UPS = 'PERP-UPS'
df_ups_assets = pd.read_csv(STAGING_ASSETS_DIR / f'{SUB_UPS}.csv', dtype=str)
df_ups_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_UPS}.csv', dtype=str)

TARGET_UPS = [
    ('174', 'UPS 10 kVA', '10.000 VA', [2598]),
    ('64', 'UPS 6000 VA', '6.000 VA', [3949]),
    ('174', 'UPS SIN 3100', '5.000 VA', [3950, 3951, 3952]),
    ('86', 'Smart-UPS 5000', '5.000 VA', [6520])
]

sub_barangs_ups = []
sub_lots_ups = []
ups_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_UPS, start=1):
    barang_num = f'{SUB_UPS}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_UPS],
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
    sub_barangs_ups.append(b_dict)
    sub_lots_ups.append(l_dict)
    for aid in aids:
        ups_unit_lot_map[str(aid)] = (seq_counter, spec_val)

df_sub_b_ups = pd.DataFrame(sub_barangs_ups)
df_sub_l_ups = pd.DataFrame(sub_lots_ups)
df_sub_b_ups.to_csv(STAGING_BARANGS_DIR / f'{SUB_UPS}.csv', index=False)
df_sub_l_ups.to_csv(STAGING_LOTS_DIR / f'{SUB_UPS}.csv', index=False)

for idx in df_ups_units.index:
    aid = str(df_ups_units.at[idx, 'ams_asset_id']).strip()
    if aid in ups_unit_lot_map:
        lot_id, spec = ups_unit_lot_map[aid]
        df_ups_units.at[idx, 'lot_id'] = lot_id
        df_ups_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_ups_units.columns:
        df_ups_units[c] = pd.to_numeric(df_ups_units[c], errors='coerce').astype('Int64')
df_ups_units.to_csv(STAGING_UNITS_DIR / f'{SUB_UPS}.csv', index=False)

# 2. PERP-VGA
SUB_VGA = 'PERP-VGA'
df_vga_assets = pd.read_csv(STAGING_ASSETS_DIR / f'{SUB_VGA}.csv', dtype=str)
df_vga_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_VGA}.csv', dtype=str)

TARGET_VGA = [
    ('44', 'Quadro FX 580', '512 MB', [3247]),
    ('67', 'GeForce GTX 980', '4 GB', [3975, 3977])
]

sub_barangs_vga = []
sub_lots_vga = []
vga_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_VGA, start=1):
    barang_num = f'{SUB_VGA}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_VGA],
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
    sub_barangs_vga.append(b_dict)
    sub_lots_vga.append(l_dict)
    for aid in aids:
        vga_unit_lot_map[str(aid)] = (seq_counter, spec_val)

df_sub_b_vga = pd.DataFrame(sub_barangs_vga)
df_sub_l_vga = pd.DataFrame(sub_lots_vga)
df_sub_b_vga.to_csv(STAGING_BARANGS_DIR / f'{SUB_VGA}.csv', index=False)
df_sub_l_vga.to_csv(STAGING_LOTS_DIR / f'{SUB_VGA}.csv', index=False)

for idx in df_vga_units.index:
    aid = str(df_vga_units.at[idx, 'ams_asset_id']).strip()
    if aid in vga_unit_lot_map:
        lot_id, spec = vga_unit_lot_map[aid]
        df_vga_units.at[idx, 'lot_id'] = lot_id
        df_vga_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_vga_units.columns:
        df_vga_units[c] = pd.to_numeric(df_vga_units[c], errors='coerce').astype('Int64')
df_vga_units.to_csv(STAGING_UNITS_DIR / f'{SUB_VGA}.csv', index=False)

sync_consolidated_masters()

assert len(df_sub_b_ups) == 4, f'Expected 4 barangs in PERP-UPS, got {len(df_sub_b_ups)}'
assert len(df_ups_units) == 6, f'Expected 6 units in PERP-UPS, got {len(df_ups_units)}'
assert len(df_sub_b_vga) == 2, f'Expected 2 barangs in PERP-VGA, got {len(df_sub_b_vga)}'
assert len(df_vga_units) == 3, f'Expected 3 units in PERP-VGA, got {len(df_vga_units)}'
print("[SUCCESS] PERP-UPS and PERP-VGA successfully consolidated and verified.")
""")

# -----------------------------------------------------------------------------
# Section 65: PRNT-DOT, PRNT-IDC, PRNT-INK
# -----------------------------------------------------------------------------
s65_md = make_md_cell("cell_s65_md", """---
## 65. Subcategories PRNT-DOT, PRNT-IDC & PRNT-INK Consolidation
### Dot Matrix Duplicate Merge & Printer Normalization

- `PRNT-DOT`: Consolidates from 3 down to **2 master barangs** across all 3 units by merging `0002` and `0003` into `LQ-300` (`Dot Matrix A4, Monokrom`), keeping `LX-300` (`Dot Matrix A4, Monokrom`).
- `PRNT-IDC`: Preserves 1 master barang across 1 unit (`Printer ID Card`, Brand: Datacard [50]), setting specification to `NULL` to eliminate redundancy with the item name.
- `PRNT-INK`: Standardizes Title Case and model names without further consolidation (`Deskjet A3`, `Stylus A3`, `Deskjet 9100`, `Deskjet 3340`, `Stylus Photo`, `L1300`, `L805`, `Deskjet Kecil`). Preserves all 8 master barangs across 8 units.
""")

s65_code = make_code_cell("cell_s65_code", """# =============================================================================
# 65. PRNT-DOT, PRNT-IDC & PRNT-INK Consolidation
# =============================================================================
print("\\n" + "=" * 80)
print("Consolidating PRNT-DOT, PRNT-IDC & PRNT-INK")
print("=" * 80 + "\\n")

# 1. PRNT-DOT
SUB_DOT = 'PRNT-DOT'
df_dot_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_DOT}.csv', dtype=str)

TARGET_DOT = [
    ('11', 'LX-300', 'Dot Matrix A4, Monokrom', [2649]),
    ('11', 'LQ-300', 'Dot Matrix A4, Monokrom', [3011, 3477])
]

sub_barangs_dot = []
sub_lots_dot = []
dot_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_DOT, start=1):
    barang_num = f'{SUB_DOT}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_DOT],
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
    sub_barangs_dot.append(b_dict)
    sub_lots_dot.append(l_dict)
    for aid in aids:
        dot_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_dot).to_csv(STAGING_BARANGS_DIR / f'{SUB_DOT}.csv', index=False)
pd.DataFrame(sub_lots_dot).to_csv(STAGING_LOTS_DIR / f'{SUB_DOT}.csv', index=False)

for idx in df_dot_units.index:
    aid = str(df_dot_units.at[idx, 'ams_asset_id']).strip()
    if aid in dot_unit_lot_map:
        lot_id, spec = dot_unit_lot_map[aid]
        df_dot_units.at[idx, 'lot_id'] = lot_id
        df_dot_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_dot_units.columns:
        df_dot_units[c] = pd.to_numeric(df_dot_units[c], errors='coerce').astype('Int64')
df_dot_units.to_csv(STAGING_UNITS_DIR / f'{SUB_DOT}.csv', index=False)

# 2. PRNT-IDC
SUB_IDC = 'PRNT-IDC'
df_idc_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_IDC}.csv', dtype=str)

TARGET_IDC = [
    ('50', 'Printer ID Card', None, [3563])
]

sub_barangs_idc = []
sub_lots_idc = []
idc_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_IDC, start=1):
    barang_num = f'{SUB_IDC}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_IDC],
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
    sub_barangs_idc.append(b_dict)
    sub_lots_idc.append(l_dict)
    for aid in aids:
        idc_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_idc).to_csv(STAGING_BARANGS_DIR / f'{SUB_IDC}.csv', index=False)
pd.DataFrame(sub_lots_idc).to_csv(STAGING_LOTS_DIR / f'{SUB_IDC}.csv', index=False)

for idx in df_idc_units.index:
    aid = str(df_idc_units.at[idx, 'ams_asset_id']).strip()
    if aid in idc_unit_lot_map:
        lot_id, spec = idc_unit_lot_map[aid]
        df_idc_units.at[idx, 'lot_id'] = lot_id
        df_idc_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_idc_units.columns:
        df_idc_units[c] = pd.to_numeric(df_idc_units[c], errors='coerce').astype('Int64')
df_idc_units.to_csv(STAGING_UNITS_DIR / f'{SUB_IDC}.csv', index=False)

# 3. PRNT-INK
SUB_INK = 'PRNT-INK'
df_ink_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_INK}.csv', dtype=str)

TARGET_INK = [
    ('9', 'Deskjet A3', 'A3, Color', [2637]),
    ('11', 'Stylus A3', 'A3, Color', [2638]),
    ('9', 'Deskjet 9100', 'A4, Color', [2994]),
    ('9', 'Deskjet 3340', 'A4, Color', [3003]),
    ('11', 'Stylus Photo', 'A4, Color', [3010]),
    ('11', 'L1300', 'A3 Inkjet', [5260]),
    ('11', 'L805', 'A4 Inkjet, Ink Tank', [7902]),
    ('9', 'Deskjet Kecil', None, [8611])
]

sub_barangs_ink = []
sub_lots_ink = []
ink_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_INK, start=1):
    barang_num = f'{SUB_INK}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_INK],
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
    sub_barangs_ink.append(b_dict)
    sub_lots_ink.append(l_dict)
    for aid in aids:
        ink_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_ink).to_csv(STAGING_BARANGS_DIR / f'{SUB_INK}.csv', index=False)
pd.DataFrame(sub_lots_ink).to_csv(STAGING_LOTS_DIR / f'{SUB_INK}.csv', index=False)

for idx in df_ink_units.index:
    aid = str(df_ink_units.at[idx, 'ams_asset_id']).strip()
    if aid in ink_unit_lot_map:
        lot_id, spec = ink_unit_lot_map[aid]
        df_ink_units.at[idx, 'lot_id'] = lot_id
        df_ink_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_ink_units.columns:
        df_ink_units[c] = pd.to_numeric(df_ink_units[c], errors='coerce').astype('Int64')
df_ink_units.to_csv(STAGING_UNITS_DIR / f'{SUB_INK}.csv', index=False)

sync_consolidated_masters()

assert len(sub_barangs_dot) == 2, f'Expected 2 barangs in PRNT-DOT, got {len(sub_barangs_dot)}'
assert len(df_dot_units) == 3, f'Expected 3 units in PRNT-DOT, got {len(df_dot_units)}'
assert len(sub_barangs_idc) == 1, f'Expected 1 barang in PRNT-IDC, got {len(sub_barangs_idc)}'
assert len(df_idc_units) == 1, f'Expected 1 unit in PRNT-IDC, got {len(df_idc_units)}'
assert len(sub_barangs_ink) == 8, f'Expected 8 barangs in PRNT-INK, got {len(sub_barangs_ink)}'
assert len(df_ink_units) == 8, f'Expected 8 units in PRNT-INK, got {len(df_ink_units)}'
print("[SUCCESS] PRNT-DOT, PRNT-IDC, and PRNT-INK successfully consolidated and verified.")
""")

# -----------------------------------------------------------------------------
# Section 66: PRNT-LJT, PRNT-MLT, PRNT-PLT
# -----------------------------------------------------------------------------
s66_md = make_md_cell("cell_s66_md", """---
## 66. Subcategories PRNT-LJT, PRNT-MLT & PRNT-PLT Consolidation
### LaserJet, Multifunction, and Plotter Normalization

- `PRNT-LJT`: Standardizes model designations (`LaserJet 1200`, `LaserJet 5100`, `LaserJet 6L`, `LaserJet 5500`, `LaserJet 5200`, `Phaser 3200MFP`, `Phaser 3125N`, `LaserJet 5200L`) into item names without brand repetition, and moves technical parameters (Paper size, Color/Monokrom, Network) into specifications. Preserves all 8 master barangs across 19 units.
- `PRNT-MLT`: Cleans brand repetition, standardizes Title Case and multifunction specifications (`OfficeJet 4500`, `OfficeJet 4500 Color`, `Deskjet 2050 All-in-One`, `Deskjet 2545 All-in-One`, `Ink Tank Wireless 415`, `EcoTank L3150 Wi-Fi`). Preserves all 6 master barangs across 9 units.
- `PRNT-PLT`: Consolidates from 2 down to **1 master barang** across all 2 units by merging `0001` (`Xerox 8830 Plotter A0`) and `0002` (`Xerox A0`) into `Plotter 8830` (`Format Lebar A0, Monokrom`).
""")

s66_code = make_code_cell("cell_s66_code", """# =============================================================================
# 66. PRNT-LJT, PRNT-MLT & PRNT-PLT Consolidation
# =============================================================================
print("\\n" + "=" * 80)
print("Consolidating PRNT-LJT, PRNT-MLT & PRNT-PLT")
print("=" * 80 + "\\n")

# 1. PRNT-LJT
SUB_LJT = 'PRNT-LJT'
df_ljt_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_LJT}.csv', dtype=str)

TARGET_LJT = [
    ('9', 'LaserJet 1200', 'A4, Monokrom', [2636]),
    ('9', 'LaserJet 5100', 'A3, Monokrom, Network', [2648, 2651, 2652, 2653, 2654, 2655, 2656, 2657, 2658, 2967]),
    ('9', 'LaserJet 6L', 'A4, Monokrom', [2650]),
    ('9', 'LaserJet 5500', 'A3, Color, Network', [2995]),
    ('9', 'LaserJet 5200', 'A3, Monokrom, Network', [3135]),
    ('16', 'Phaser 3200MFP', 'Laser Multifungsi (Print, Scan, Copy, Fax)', [3198, 3235]),
    ('16', 'Phaser 3125N', 'Laser A4, Network', [3238, 3246]),
    ('9', 'LaserJet 5200L', 'A3, Monokrom', [3780])
]

sub_barangs_ljt = []
sub_lots_ljt = []
ljt_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_LJT, start=1):
    barang_num = f'{SUB_LJT}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_LJT],
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
    sub_barangs_ljt.append(b_dict)
    sub_lots_ljt.append(l_dict)
    for aid in aids:
        ljt_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_ljt).to_csv(STAGING_BARANGS_DIR / f'{SUB_LJT}.csv', index=False)
pd.DataFrame(sub_lots_ljt).to_csv(STAGING_LOTS_DIR / f'{SUB_LJT}.csv', index=False)

for idx in df_ljt_units.index:
    aid = str(df_ljt_units.at[idx, 'ams_asset_id']).strip()
    if aid in ljt_unit_lot_map:
        lot_id, spec = ljt_unit_lot_map[aid]
        df_ljt_units.at[idx, 'lot_id'] = lot_id
        df_ljt_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_ljt_units.columns:
        df_ljt_units[c] = pd.to_numeric(df_ljt_units[c], errors='coerce').astype('Int64')
df_ljt_units.to_csv(STAGING_UNITS_DIR / f'{SUB_LJT}.csv', index=False)

# 2. PRNT-MLT
SUB_MLT = 'PRNT-MLT'
df_mlt_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_MLT}.csv', dtype=str)

TARGET_MLT = [
    ('9', 'OfficeJet 4500', 'A4 Multifungsi (Print, Scan, Copy)', [3252]),
    ('9', 'OfficeJet 4500 Color', 'A4 Multifungsi, Color', [3257]),
    ('9', 'Deskjet 2050 All-in-One', 'A4 (Print, Scan, Copy)', [3832, 3834]),
    ('9', 'Deskjet 2545 All-in-One', 'A4 (Print, Scan, Copy)', [3837]),
    ('9', 'Ink Tank Wireless 415', 'A4 Multifungsi, Wireless', [4131, 4132, 4139]),
    ('11', 'EcoTank L3150 Wi-Fi', 'A4 Multifungsi, Wi-Fi', [5261])
]

sub_barangs_mlt = []
sub_lots_mlt = []
mlt_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_MLT, start=1):
    barang_num = f'{SUB_MLT}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_MLT],
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
    sub_barangs_mlt.append(b_dict)
    sub_lots_mlt.append(l_dict)
    for aid in aids:
        mlt_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_mlt).to_csv(STAGING_BARANGS_DIR / f'{SUB_MLT}.csv', index=False)
pd.DataFrame(sub_lots_mlt).to_csv(STAGING_LOTS_DIR / f'{SUB_MLT}.csv', index=False)

for idx in df_mlt_units.index:
    aid = str(df_mlt_units.at[idx, 'ams_asset_id']).strip()
    if aid in mlt_unit_lot_map:
        lot_id, spec = mlt_unit_lot_map[aid]
        df_mlt_units.at[idx, 'lot_id'] = lot_id
        df_mlt_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_mlt_units.columns:
        df_mlt_units[c] = pd.to_numeric(df_mlt_units[c], errors='coerce').astype('Int64')
df_mlt_units.to_csv(STAGING_UNITS_DIR / f'{SUB_MLT}.csv', index=False)

# 3. PRNT-PLT
SUB_PLT = 'PRNT-PLT'
df_plt_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_PLT}.csv', dtype=str)

TARGET_PLT = [
    ('16', 'Plotter 8830', 'Format Lebar A0, Monokrom', [2966, 3562])
]

sub_barangs_plt = []
sub_lots_plt = []
plt_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_PLT, start=1):
    barang_num = f'{SUB_PLT}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_PLT],
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
    sub_barangs_plt.append(b_dict)
    sub_lots_plt.append(l_dict)
    for aid in aids:
        plt_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_plt).to_csv(STAGING_BARANGS_DIR / f'{SUB_PLT}.csv', index=False)
pd.DataFrame(sub_lots_plt).to_csv(STAGING_LOTS_DIR / f'{SUB_PLT}.csv', index=False)

for idx in df_plt_units.index:
    aid = str(df_plt_units.at[idx, 'ams_asset_id']).strip()
    if aid in plt_unit_lot_map:
        lot_id, spec = plt_unit_lot_map[aid]
        df_plt_units.at[idx, 'lot_id'] = lot_id
        df_plt_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_plt_units.columns:
        df_plt_units[c] = pd.to_numeric(df_plt_units[c], errors='coerce').astype('Int64')
df_plt_units.to_csv(STAGING_UNITS_DIR / f'{SUB_PLT}.csv', index=False)

sync_consolidated_masters()

assert len(sub_barangs_ljt) == 8, f'Expected 8 barangs in PRNT-LJT, got {len(sub_barangs_ljt)}'
assert len(df_ljt_units) == 19, f'Expected 19 units in PRNT-LJT, got {len(df_ljt_units)}'
assert len(sub_barangs_mlt) == 6, f'Expected 6 barangs in PRNT-MLT, got {len(sub_barangs_mlt)}'
assert len(df_mlt_units) == 9, f'Expected 9 units in PRNT-MLT, got {len(df_mlt_units)}'
assert len(sub_barangs_plt) == 1, f'Expected 1 barang in PRNT-PLT, got {len(sub_barangs_plt)}'
assert len(df_plt_units) == 2, f'Expected 2 units in PRNT-PLT, got {len(df_plt_units)}'
print("[SUCCESS] PRNT-LJT, PRNT-MLT, and PRNT-PLT successfully consolidated and verified.")
""")

# -----------------------------------------------------------------------------
# Section 67: PROP-PRO
# -----------------------------------------------------------------------------
s67_md = make_md_cell("cell_s67_md", """---
## 67. Subcategory PROP-PRO Standardization & Polish
### Typo Correction & Redundancy Removal

- Standardizes building titles (`Gedung Graha RE 1`, `Gedung Graha RE 2`) and monument names (`Prasasti Gedung Graha RE 1`, `Prasasti Gedung Graha RE 2`).
- Cleans dry container naming (`Dry Container 40 Feet`), setting redundant specification to `NULL`.
- Corrects typo in `Pagar Stenlinless Top floor` (`Stenlinless` -> `Stainless`), setting redundant specification to `NULL`.
- Cleans corporate logo item (`Logo Nama Perusahaan`, Spec: `Logo RE`).
- Normalizes solar roof system (`PLTS Atap`, Spec: `On Grid 9,9 kWp`).
- Preserves all 8 master barangs across 8 units.
""")

s67_code = make_code_cell("cell_s67_code", """# =============================================================================
# 67. PROP-PRO Standardization & Polish
# =============================================================================
print("\\n" + "=" * 80)
print("Standardizing PROP-PRO")
print("=" * 80 + "\\n")

SUB_PROP = 'PROP-PRO'
df_prop_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_PROP}.csv', dtype=str)

TARGET_PROP = [
    ('95', 'Gedung Graha RE 1', None, [7998]),
    ('95', 'Gedung Graha RE 2', None, [7999]),
    ('104', 'Dry Container 40 Feet', None, [8135]),
    ('5', 'Prasasti Gedung Graha RE 1', None, [8136]),
    ('5', 'Prasasti Gedung Graha RE 2', None, [8137]),
    ('98', 'Pagar Stainless Top Floor', None, [8139]),
    ('5', 'Logo Nama Perusahaan', 'Logo RE', [8142]),
    ('100', 'PLTS Atap', 'On Grid 9,9 kWp', [8143])
]

sub_barangs_prop = []
sub_lots_prop = []
prop_unit_lot_map = {}

for seq_counter, (b_id, name_val, spec_val, aids) in enumerate(TARGET_PROP, start=1):
    barang_num = f'{SUB_PROP}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map[SUB_PROP],
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
    sub_barangs_prop.append(b_dict)
    sub_lots_prop.append(l_dict)
    for aid in aids:
        prop_unit_lot_map[str(aid)] = (seq_counter, spec_val)

pd.DataFrame(sub_barangs_prop).to_csv(STAGING_BARANGS_DIR / f'{SUB_PROP}.csv', index=False)
pd.DataFrame(sub_lots_prop).to_csv(STAGING_LOTS_DIR / f'{SUB_PROP}.csv', index=False)

for idx in df_prop_units.index:
    aid = str(df_prop_units.at[idx, 'ams_asset_id']).strip()
    if aid in prop_unit_lot_map:
        lot_id, spec = prop_unit_lot_map[aid]
        df_prop_units.at[idx, 'lot_id'] = lot_id
        df_prop_units.at[idx, 'specification'] = spec

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_prop_units.columns:
        df_prop_units[c] = pd.to_numeric(df_prop_units[c], errors='coerce').astype('Int64')
df_prop_units.to_csv(STAGING_UNITS_DIR / f'{SUB_PROP}.csv', index=False)

sync_consolidated_masters()

assert len(sub_barangs_prop) == 8, f'Expected 8 barangs in PROP-PRO, got {len(sub_barangs_prop)}'
assert len(df_prop_units) == 8, f'Expected 8 units in PROP-PRO, got {len(df_prop_units)}'
print("[SUCCESS] PROP-PRO successfully standardized and verified.")
""")

# -----------------------------------------------------------------------------
# Section 68: Batch Verification & Global Integrity Check
# -----------------------------------------------------------------------------
s68_md = make_md_cell("cell_s68_md", """---
## 68. Peripheral, Printer & Property Batch Verification & Global Integrity Check
### Zero-Loss Validation and Master Integrity

- Rigorously validates all 9 subcategories in the batch (`PERP-UPS`, `PERP-VGA`, `PRNT-DOT`, `PRNT-IDC`, `PRNT-INK`, `PRNT-LJT`, `PRNT-MLT`, `PRNT-PLT`, `PROP-PRO`).
- Verifies system-wide invariants: exactly **667 master barangs**, **667 master lots**, and **6,939 master units** preserved 100%.
""")

s68_code = make_code_cell("cell_s68_code", """# =============================================================================
# 68. Peripheral, Printer & Property Batch Verification & Global Integrity Check
# =============================================================================
print("\\n" + "=" * 80)
print("Verifying Peripheral, Printer & Property Batch Masters & System-Wide Invariants")
print("=" * 80 + "\\n")

expected_units_batch2 = {
    'PERP-UPS': 6,
    'PERP-VGA': 3,
    'PRNT-DOT': 3,
    'PRNT-IDC': 1,
    'PRNT-INK': 8,
    'PRNT-LJT': 19,
    'PRNT-MLT': 9,
    'PRNT-PLT': 2,
    'PROP-PRO': 8
}

for sub_c, exp_count in expected_units_batch2.items():
    df_u_part = pd.read_csv(STAGING_UNITS_DIR / f'{sub_c}.csv')
    df_b_part = pd.read_csv(STAGING_BARANGS_DIR / f'{sub_c}.csv')
    df_l_part = pd.read_csv(STAGING_LOTS_DIR / f'{sub_c}.csv')
    assert len(df_u_part) == exp_count, f"Mismatch in {sub_c}: expected {exp_count} units, got {len(df_u_part)}"
    assert len(df_b_part) == len(df_l_part), f"Barangs vs Lots mismatch in {sub_c}: {len(df_b_part)} vs {len(df_l_part)}"
    assert df_u_part['lot_id'].isin(df_l_part['id']).all(), f"Invalid lot_id found in {sub_c} units!"

# Global Master Tables
df_barangs_m = pd.read_csv(FINAL_BARANG_DIR / 'barangs.csv')
df_lots_m = pd.read_csv(FINAL_LOT_DIR / 'lots.csv')
df_units_m = pd.read_csv(FINAL_UNIT_DIR / 'units.csv')

assert len(df_barangs_m) == 667, f"Expected 667 barangs, got {len(df_barangs_m)}"
assert len(df_lots_m) == 667, f"Expected 667 lots, got {len(df_lots_m)}"
assert len(df_units_m) == 6939, f"Expected 6,939 units, got {len(df_units_m)}"

assert (df_barangs_m['id'].astype(int) == list(range(1, len(df_barangs_m) + 1))).all()
assert (df_lots_m['id'].astype(int) == list(range(1, len(df_lots_m) + 1))).all()
assert df_barangs_m['number'].is_unique
assert df_lots_m['number'].is_unique

print("[SUCCESS] All Peripheral, Printer & Property batch and system-wide assertions passed successfully!")
print(f"Master barangs: {len(df_barangs_m):,}")
print(f"Master lots:    {len(df_lots_m):,}")
print(f"Master units:   {len(df_units_m):,}")
""")

new_cells = [
    s64_md, s64_code,
    s65_md, s65_code,
    s66_md, s66_code,
    s67_md, s67_code,
    s68_md, s68_code
]

# Verify compilation of all code cells
for i, c in enumerate(new_cells):
    if c['cell_type'] == 'code':
        src = "".join(c['source'])
        compile(src, f'<new_cell_{i}>', 'exec')
print("All new cells compiled with ZERO syntax errors.")

nb['cells'].extend(new_cells)

with open('notebooks/09_barang_consolidation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Appended 10 new cells (Sections 64 through 68). Total notebook cells: {len(nb['cells'])}.")
