import json

nb_path = 'notebooks/09_barang_consolidation.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Helper to build code cell cleanly
def make_code_cell(cid, code_str):
    lines = [l + '\n' for l in code_str.strip().split('\n')[:-1]] + [code_str.strip().split('\n')[-1]]
    return {
        'cell_type': 'code',
        'execution_count': None,
        'id': cid,
        'metadata': {},
        'outputs': [],
        'source': lines
    }

def make_md_cell(cid, md_str):
    lines = [l + '\n' for l in md_str.strip().split('\n')[:-1]] + [md_str.strip().split('\n')[-1]]
    return {
        'cell_type': 'markdown',
        'id': cid,
        'metadata': {},
        'source': lines
    }

# -----------------------------------------------------------------------------
# Section 57: PERP-ACCN & ELEK-FR
# -----------------------------------------------------------------------------
s57_md = make_md_cell('cell_s57_md', """---
## 57. Subcategory PERP-ACCN & ELEK-FR Consolidation
### Fingerprint Reader Relocation & Access Control Typo Correction

- Relocates 3 units of Solution M100 biometric fingerprint readers from `PERP-ACCN` to `ELEK-FR` (`ELEK-FR-0003`).
- Corrects typo in `PERP-ACCN-0001` (formerly 0002) specification (`MAKNETIK` -> `Magnetik`).
- `PERP-ACCN`: 1 master barang across 3 units.
- `ELEK-FR`: 3 master barangs across 7 units.
""")

s57_code = make_code_cell('cell_s57_code', """# =============================================================================
# 57. PERP-ACCN & ELEK-FR Consolidation & Transfer
# =============================================================================
print(f"\\n{'='*80}")
print("Consolidating PERP-ACCN & Transferring Biometrics to ELEK-FR")
print(f"{'='*80}\\n")

df_accn_units = pd.read_csv(STAGING_UNITS_DIR / 'PERP-ACCN.csv')
df_fr_units = pd.read_csv(STAGING_UNITS_DIR / 'ELEK-FR.csv')

# Assets to transfer to ELEK-FR
m100_aids = [2978, 2984, 2986]

# 1. Update ELEK-FR
TARGET_FR = [
    ('124', 'Fingkey Access', None),
    ('133', 'Fingerprint (Lawas)', None),
    ('133', 'M100', 'Mesin Absensi Sidik Jari, LAN')
]

sub_barangs_fr = []
sub_lots_fr = []

for seq_counter, (b_id, name_val, spec_val) in enumerate(TARGET_FR, start=1):
    barang_num = f'ELEK-FR-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    b_dict = {
        'id': seq_counter, 'number': barang_num, 'subcategory_id': sub_map['ELEK-FR'],
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
    sub_barangs_fr.append(b_dict)
    sub_lots_fr.append(l_dict)

pd.DataFrame(sub_barangs_fr).to_csv(STAGING_BARANGS_DIR / 'ELEK-FR.csv', index=False)
pd.DataFrame(sub_lots_fr).to_csv(STAGING_LOTS_DIR / 'ELEK-FR.csv', index=False)

# Transfer units: extract from ACCN and append to FR
m100_rows = df_accn_units[df_accn_units['ams_asset_id'].isin(m100_aids)].copy()
m100_rows['subcategory_code'] = 'ELEK-FR'
m100_rows['lot_id'] = 3
m100_rows['specification'] = 'Mesin Absensi Sidik Jari, LAN'

for idx in df_fr_units.index:
    aid = int(df_fr_units.at[idx, 'ams_asset_id'])
    if aid in [8666, 8684, 11837]:
        df_fr_units.at[idx, 'lot_id'] = 1
        df_fr_units.at[idx, 'specification'] = None
    elif aid == 8948:
        df_fr_units.at[idx, 'lot_id'] = 2
        df_fr_units.at[idx, 'specification'] = None

df_fr_units_new = pd.concat([df_fr_units, m100_rows], ignore_index=True)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_fr_units_new.columns:
        df_fr_units_new[c] = pd.to_numeric(df_fr_units_new[c], errors='coerce').astype('Int64')
df_fr_units_new.to_csv(STAGING_UNITS_DIR / 'ELEK-FR.csv', index=False)

# 2. Update PERP-ACCN
df_accn_units_remain = df_accn_units[~df_accn_units['ams_asset_id'].isin(m100_aids)].copy()

sub_barangs_accn = [{
    'id': 1, 'number': 'PERP-ACCN-0001', 'subcategory_id': sub_map['PERP-ACCN'],
    'brand_id': '26', 'uom_id': 1, 'name': 'Accessnetic', 'specification': 'Mesin Akses Kontrol Magnetik',
    'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
    'created_at': now_str, 'updated_at': now_str
}]
sub_lots_accn = [{
    'id': 1, 'number': 'LOT-0001-26-PERP-ACCN-0001', 'barang_id': 1,
    'organizer_id': 1, 'vendor_id': None, 'legacy_vendor_id': None,
    'location_id': None, 'initial_quantity': None, 'current_quantity': None,
    'po_number': None, 'date_of_receipt': now_str, 'unit_price': None,
    'image_url': None, 'burden': None, 'project_id': None,
    'created_at': now_str, 'updated_at': now_str
}]

pd.DataFrame(sub_barangs_accn).to_csv(STAGING_BARANGS_DIR / 'PERP-ACCN.csv', index=False)
pd.DataFrame(sub_lots_accn).to_csv(STAGING_LOTS_DIR / 'PERP-ACCN.csv', index=False)

df_accn_units_remain['lot_id'] = 1
df_accn_units_remain['specification'] = 'Mesin Akses Kontrol Magnetik'
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_accn_units_remain.columns:
        df_accn_units_remain[c] = pd.to_numeric(df_accn_units_remain[c], errors='coerce').astype('Int64')
df_accn_units_remain.to_csv(STAGING_UNITS_DIR / 'PERP-ACCN.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(sub_barangs_accn) == 1, f"Expected 1 ACCN barang, got {len(sub_barangs_accn)}"
assert len(df_accn_units_remain) == 3, f"Expected 3 ACCN units, got {len(df_accn_units_remain)}"
assert len(sub_barangs_fr) == 3, f"Expected 3 FR barangs, got {len(sub_barangs_fr)}"
assert len(df_fr_units_new) == 7, f"Expected 7 FR units, got {len(df_fr_units_new)}"
print(f"\\n[SUCCESS] Consolidated PERP-ACCN (1 barang, 3 units) & ELEK-FR (3 barangs, 7 units).")
""")

# -----------------------------------------------------------------------------
# Section 58: PERP-ACCS, PERP-CAM, PERP-COMM
# -----------------------------------------------------------------------------
s58_md = make_md_cell('cell_s58_md', """---
## 58. Subcategories PERP-ACCS, PERP-CAM & PERP-COMM Standardization
### Peripheral Accessories, Cameras, and Communications Equipment

- `PERP-ACCS`: Standardizes formatting, removes redundant brand names, and fixes typos (3 barangs across 3 units).
- `PERP-CAM`: Standardizes camera models, removes redundant brand names from item names, and formats specs in Title Case (9 barangs across 10 units).
- `PERP-COMM`: Standardizes communication devices (modem, IP phone, conference system) and removes brand redundancy (4 barangs across 16 units).
""")

s58_code = make_code_cell('cell_s58_code', """# =============================================================================
# 58. PERP-ACCS, PERP-CAM, PERP-COMM Standardization
# =============================================================================
print(f"\\n{'='*80}")
print("Standardizing PERP-ACCS, PERP-CAM, PERP-COMM")
print(f"{'='*80}\\n")

# --- 1. PERP-ACCS ---
df_accs_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-ACCS.csv')
TARGET_ACCS = [
    ('41', 'Laser Pointer', 'With Mouse Function', [3189]),
    ('45', 'Converter USB', 'USB to 140016', [3258]),
    ('83', 'Bangunan Graha RE 1', None, [7899])
]
sub_barangs_accs = []
sub_lots_accs = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_ACCS, start=1):
    bnum = f'PERP-ACCS-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_accs.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-ACCS'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_accs.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_accs_u[df_accs_u['ams_asset_id'].isin(aids)].index:
        df_accs_u.at[idx, 'lot_id'] = seq
        df_accs_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_accs).to_csv(STAGING_BARANGS_DIR / 'PERP-ACCS.csv', index=False)
pd.DataFrame(sub_lots_accs).to_csv(STAGING_LOTS_DIR / 'PERP-ACCS.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_accs_u.columns: df_accs_u[c] = pd.to_numeric(df_accs_u[c], errors='coerce').astype('Int64')
df_accs_u.to_csv(STAGING_UNITS_DIR / 'PERP-ACCS.csv', index=False)

# --- 2. PERP-CAM ---
df_cam_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-CAM.csv')
TARGET_CAM = [
    ('17', 'Ixus', 'Kamera Kompak', [2981]),
    ('17', 'EOS', 'Kamera DSLR', [2985]),
    ('123', 'Network Camera', 'Akses Network LAN', [2991, 2992]),
    ('20', 'Desktop Camera', 'Dokumen Kamera', [2999]),
    ('15', 'Handycam', 'DVD', [3048]),
    ('90', 'Mavic 3 Classic', 'Paket with RC', [8038]),
    ('91', 'Hero 10 Black', None, [8083]),
    ('92', 'Brave 7 LE', 'Sensor Sony IMX386, 4K 30fps, 20MP, Waterproof IPX7', [8105]),
    ('169', 'D3200', 'Baterai 2 Unit', [11963])
]
sub_barangs_cam = []
sub_lots_cam = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_CAM, start=1):
    bnum = f'PERP-CAM-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_cam.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-CAM'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_cam.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_cam_u[df_cam_u['ams_asset_id'].isin(aids)].index:
        df_cam_u.at[idx, 'lot_id'] = seq
        df_cam_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_cam).to_csv(STAGING_BARANGS_DIR / 'PERP-CAM.csv', index=False)
pd.DataFrame(sub_lots_cam).to_csv(STAGING_LOTS_DIR / 'PERP-CAM.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_cam_u.columns: df_cam_u[c] = pd.to_numeric(df_cam_u[c], errors='coerce').astype('Int64')
df_cam_u.to_csv(STAGING_UNITS_DIR / 'PERP-CAM.csv', index=False)

# --- 3. PERP-COMM ---
df_comm_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-COMM.csv')
TARGET_COMM = [
    ('38', 'Modem 3G GSM Portable', 'USB', [3180, 3181, 3182]),
    ('40', 'IP Phone SIP', None, [3185, 3186, 3187, 3188]),
    ('72', 'SoundStation 2', 'Non-Expandable', [4056, 4057, 4058, 4059, 4060]),
    ('71', 'Group', 'Video Conference', [4061, 4062, 4063, 4064])
]
sub_barangs_comm = []
sub_lots_comm = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_COMM, start=1):
    bnum = f'PERP-COMM-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_comm.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-COMM'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_comm.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_comm_u[df_comm_u['ams_asset_id'].isin(aids)].index:
        df_comm_u.at[idx, 'lot_id'] = seq
        df_comm_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_comm).to_csv(STAGING_BARANGS_DIR / 'PERP-COMM.csv', index=False)
pd.DataFrame(sub_lots_comm).to_csv(STAGING_LOTS_DIR / 'PERP-COMM.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_comm_u.columns: df_comm_u[c] = pd.to_numeric(df_comm_u[c], errors='coerce').astype('Int64')
df_comm_u.to_csv(STAGING_UNITS_DIR / 'PERP-COMM.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(sub_barangs_accs) == 3 and len(df_accs_u) == 3
assert len(sub_barangs_cam) == 9 and len(df_cam_u) == 10
assert len(sub_barangs_comm) == 4 and len(df_comm_u) == 16
print(f"\\n[SUCCESS] Standardized PERP-ACCS (3), PERP-CAM (9), PERP-COMM (4).")
""")

# -----------------------------------------------------------------------------
# Section 59: PERP-MEXT & PERP-MMD
# -----------------------------------------------------------------------------
s59_md = make_md_cell('cell_s59_md', """---
## 59. Subcategories PERP-MEXT & PERP-MMD Consolidation
### External Storage Consolidation & Multimedia Device Deduplication

- `PERP-MEXT`: Consolidates 19 legacy barangs down to 16 master barangs across 24 units. Merges 3 Seagate 1TB external HDD entries and 2 Seagate One Touch 4TB entries.
- `PERP-MMD`: Consolidates 6 legacy barangs down to 5 master barangs across 6 units. Combines contiguous Panasonic Panaboard entries `0003` & `0004` into `Panaboard 5220` with spec `Papan Tulis Elektrik (900 x 400)`. Corrects typos (`BOSC`, `TUNNER`, `Celing`).
""")

s59_code = make_code_cell('cell_s59_code', """# =============================================================================
# 59. PERP-MEXT & PERP-MMD Consolidation
# =============================================================================
print(f"\\n{'='*80}")
print("Consolidating PERP-MEXT & PERP-MMD")
print(f"{'='*80}\\n")

# --- 1. PERP-MEXT ---
df_mext_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-MEXT.csv')
TARGET_MEXT = [
    ('3', 'CDRW External 24x', None, [2599, 2603]),
    ('15', 'DVDRW External 4x', None, [2751]),
    ('21', 'DVDRW External 8x', None, [2997, 3012, 3052, 3142]),
    ('8', 'HDD External 80GB', '2.5"', [3006]),
    ('8', 'HDD External 160GB', '2.5"', [3013]),
    ('24', 'HDD External SAN', 'Fasilitas Networking', [3020]),
    ('9', 'Tape Backup External', None, [3071]),
    ('43', 'HDD External 500GB', '2.5" Anti-Shock', [3245]),
    ('84', 'HDD External 1TB', None, [7906, 7907, 7908]), # Merged 0009, 0010, 0011
    ('84', 'SSD External 500GB', 'Expansion SSD', [8147]),
    ('84', 'HDD External 8TB', 'One Touch Desktop Hub, USB 3.0', [8149]),
    ('84', 'HDD External 4TB', 'One Touch 3.5"', [10649, 11904]), # Merged 0017, 0018
    ('29', 'SSD External 1TB', None, [7913]),
    ('29', 'SSD External 500GB', None, [7914]),
    ('110', 'SSD External 1TB', 'Enclosure Orico', [8268, 8269]),
    ('168', 'HDD Docking Bay 9848U3', '4 Slot', [11949])
]
sub_barangs_mext = []
sub_lots_mext = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_MEXT, start=1):
    bnum = f'PERP-MEXT-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_mext.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-MEXT'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_mext.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_mext_u[df_mext_u['ams_asset_id'].isin(aids)].index:
        df_mext_u.at[idx, 'lot_id'] = seq
        df_mext_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_mext).to_csv(STAGING_BARANGS_DIR / 'PERP-MEXT.csv', index=False)
pd.DataFrame(sub_lots_mext).to_csv(STAGING_LOTS_DIR / 'PERP-MEXT.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_mext_u.columns: df_mext_u[c] = pd.to_numeric(df_mext_u[c], errors='coerce').astype('Int64')
df_mext_u.to_csv(STAGING_UNITS_DIR / 'PERP-MEXT.csv', index=False)

# --- 2. PERP-MMD ---
df_mmd_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-MMD.csv')
TARGET_MMD = [
    ('14', 'Home Theater', 'Audio Video DVD Player', [2659]),
    ('15', 'Video Player VHS', 'TV Tuner', [2660]),
    ('25', 'Panaboard 5220', 'Papan Tulis Elektrik (900 x 400)', [3005, 3712]), # Merged 0003, 0004
    ('54', 'CCS 900', '16 Unit', [3715]),
    ('55', 'VM-2240 & RM-200M', 'Power Amplifier 240W, Mic Remote, Ceiling Speaker', [3745])
]
sub_barangs_mmd = []
sub_lots_mmd = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_MMD, start=1):
    bnum = f'PERP-MMD-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_mmd.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-MMD'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_mmd.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_mmd_u[df_mmd_u['ams_asset_id'].isin(aids)].index:
        df_mmd_u.at[idx, 'lot_id'] = seq
        df_mmd_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_mmd).to_csv(STAGING_BARANGS_DIR / 'PERP-MMD.csv', index=False)
pd.DataFrame(sub_lots_mmd).to_csv(STAGING_LOTS_DIR / 'PERP-MMD.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_mmd_u.columns: df_mmd_u[c] = pd.to_numeric(df_mmd_u[c], errors='coerce').astype('Int64')
df_mmd_u.to_csv(STAGING_UNITS_DIR / 'PERP-MMD.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(sub_barangs_mext) == 16 and len(df_mext_u) == 24
assert len(sub_barangs_mmd) == 5 and len(df_mmd_u) == 6
print(f"\\n[SUCCESS] Consolidated PERP-MEXT (16 barangs, 24 units) & PERP-MMD (5 barangs, 6 units).")
""")

# -----------------------------------------------------------------------------
# Section 60: PERP-NETW
# -----------------------------------------------------------------------------
s60_md = make_md_cell('cell_s60_md', """---
## 60. Subcategory PERP-NETW Consolidation
### Network Switches, Routers, Firewalls, and Access Points Consolidation

- Strips location strings (`lantai 1 RETO`).
- Consolidates 34 legacy barangs down to 25 master barangs across 86 units.
- Merges 5 duplicate Ubiquiti UniFi UAP-AC-PRO entries across 32 units into 1 master item.
- Merges duplicate D-Link and TP-Link switches and routers.
- Moves lengthy technical specifications from item names to specifications (FortiGate-100F).
""")

s60_code = make_code_cell('cell_s60_code', """# =============================================================================
# 60. PERP-NETW Consolidation
# =============================================================================
print(f"\\n{'='*80}")
print("Consolidating PERP-NETW")
print(f"{'='*80}\\n")

df_netw_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-NETW.csv')

TARGET_NETW = [
    # D-Link (4)
    ('4', 'Switch DES-1016D', '16 Port 10/100 Mbps', [2600, 3143]), # 0001, 0005
    ('4', 'Switch DES-1024D', '24 Port 10/100 Mbps', [3179, 3183, 3205, 3256]), # 0006, 0008, 0010
    ('4', 'Switch DES-1026G', '24 Port 10/100 Mbps + 2 Port Gigabit', [3000, 3015, 3049, 3136, 3255]), # 0004, 0009
    ('4', 'Wireless Router DIR-615', 'Access Point + 4 Port Switch', [3197]), # 0007
    # 3Com (12)
    ('12', 'Switch SuperStack 3', '24 Port 10/100 Mbps', [2641, 2933, 2934, 2935, 2948, 2968, 2969, 2972, 2973, 2974, 2975, 2976]), # 0002
    ('12', 'Switch 8 Port', '10/100 Mbps', [2970, 2971, 2977]), # 0003
    # Panasonic (25)
    ('25', 'PABX KX-TDA200', '8 CO Line, 16 Digital, 64 Analog', [3374]), # 0011
    # HP (9)
    ('9', 'Switch ProCurve 2610-48', '48 Port 10/100 + 2 Port Gigabit, Managed', [3375, 3376, 3377, 3379, 3493]), # 0012
    ('9', 'Switch ProCurve 2520-24', '24 Port Gigabit PoE, Managed', [3378]), # 0013
    # MikroTik (47)
    ('47', 'Router RB1100AHx2', '13 Port Gigabit', [3472]), # 0014
    ('47', 'Router CCR1016', '12 Port SFP, 1 SFP+', [3958, 3959]), # 0018
    ('47', 'Router CCR1009', None, [6253]), # 0024
    ('47', 'mANTBox', 'Antena Point to Point', [6551, 6552]), # 0028
    ('47', 'Router', None, [7860]), # 0029
    # Linksys (48)
    ('48', 'Wireless Router E1500', 'Access Point Wi-Fi Hotspot', [3473]), # 0015
    # Cisco (53)
    ('53', 'Switch Catalyst 2960', '48 Port 10/100', [3714]), # 0016
    ('53', 'Switch Catalyst 2960-X', '48 Port Gigabit', [6439]), # 0027
    ('53', 'Switch Catalyst C9300L-24T-4X-E', '24 Port Data, 4x 10G Uplink', [8195]), # 0030
    # IBM (65)
    ('65', 'Switch RackSwitch G7028', '12 Port Gigabit, 2 Port SFP+', [3956, 3957]), # 0017
    # Ubiquiti (73)
    ('73', 'Access Point UniFi UAP-AC-PRO', 'Dual-Band Gigabit', [
        4129,
        6434, 6435, 6436, 6437, 6438, 6463, 6464, 6465, 6466, 6467, 6468, 6469, 6470, 6471, 6472, 6553, 6554, 6555, 6556, 6557,
        10561, 10562, 10563, 10564, 10712, 10713, 10714, 10715, 11852, 11853, 11854
    ]),
    ('73', 'Access Point UniFi UAP-AC-Lite', 'Dual-Band Gigabit', [5262]), # 0021
    # TP-Link (74)
    ('74', 'Router Archer AC9', None, [4130]), # 0020
    ('74', 'Router Archer AC2300', None, [5263, 6196, 6197]), # 0022, 0023
    # Hillstone (105)
    ('105', 'Firewall', None, [6381]), # 0025
    # Fortinet (106)
    ('106', 'Firewall FortiGate-100F', '22x GE RJ45, 4x SFP, 2x 10G SFP+, Dual Power Supply', [8196]) # 0031
]

sub_barangs_netw = []
sub_lots_netw = []

for seq, (b_id, name, spec, aids) in enumerate(TARGET_NETW, start=1):
    bnum = f'PERP-NETW-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_netw.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-NETW'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_netw.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_netw_u[df_netw_u['ams_asset_id'].isin(aids)].index:
        df_netw_u.at[idx, 'lot_id'] = seq
        df_netw_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_netw).to_csv(STAGING_BARANGS_DIR / 'PERP-NETW.csv', index=False)
pd.DataFrame(sub_lots_netw).to_csv(STAGING_LOTS_DIR / 'PERP-NETW.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_netw_u.columns: df_netw_u[c] = pd.to_numeric(df_netw_u[c], errors='coerce').astype('Int64')
df_netw_u.to_csv(STAGING_UNITS_DIR / 'PERP-NETW.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(sub_barangs_netw) == 25, f"Expected 25 NETW barangs, got {len(sub_barangs_netw)}"
assert len(df_netw_u) == 86, f"Expected 86 NETW units, got {len(df_netw_u)}"
print(f"\\n[SUCCESS] Consolidated PERP-NETW from 34 down to {len(sub_barangs_netw)} barangs across {len(df_netw_u)} units.")
""")

# -----------------------------------------------------------------------------
# Section 61: PERP-PROJ, PERP-RAKS, PERP-SCAN, PERP-SCRN
# -----------------------------------------------------------------------------
s61_md = make_md_cell('cell_s61_md', """---
## 61. Subcategories PERP-PROJ, PERP-RAKS, PERP-SCAN & PERP-SCRN Standardization
### Projectors, Server Racks, Scanners, and Presentation Screens

- `PERP-PROJ`: Standardizes 10 projector models, removes brand redundancy, and cleans specs (16 units).
- `PERP-RAKS`: Standardizes 4 server rack models and heights (6 units).
- `PERP-SCAN`: Standardizes 7 scanner models, fixes typos (`CanoScan LiDE`), and condenses technical text walls (9 units).
- `PERP-SCRN`: Standardizes 1 presentation screen with Title Casing (1 unit).
""")

s61_code = make_code_cell('cell_s61_code', """# =============================================================================
# 61. PERP-PROJ, PERP-RAKS, PERP-SCAN, PERP-SCRN Standardization
# =============================================================================
print(f"\\n{'='*80}")
print("Standardizing PERP-PROJ, PERP-RAKS, PERP-SCAN, PERP-SCRN")
print(f"{'='*80}\\n")

# --- 1. PERP-PROJ ---
df_proj_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-PROJ.csv')
TARGET_PROJ = [
    ('2', 'Projector LP-140', None, [2597]),
    ('19', 'Projector VT-S140', None, [2998]),
    ('11', 'EB-X11', 'WXGA', [3474]),
    ('11', 'EB-1761W', 'WXGA, 2800 Lumens', [3708, 3709, 3710, 3711]),
    ('11', 'EB-485W', 'WXGA, 3000 Lumens, Short Throw', [3713]),
    ('57', 'CP-EX300', 'XGA, 3200 Lumens', [3759, 3760]),
    ('63', 'Projector WXGA 3D', None, [3894, 3895]),
    ('19', 'M322X', 'WUXGA 1920 x 1200', [3963, 3964]),
    ('2', 'IN136', 'WXGA, 4000 Lumens', [7904]),
    ('96', 'LS740W', 'WXGA Laser, 5000 ANSI Lumens', [8134])
]
sub_barangs_proj = []
sub_lots_proj = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_PROJ, start=1):
    bnum = f'PERP-PROJ-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_proj.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-PROJ'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_proj.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_proj_u[df_proj_u['ams_asset_id'].isin(aids)].index:
        df_proj_u.at[idx, 'lot_id'] = seq
        df_proj_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_proj).to_csv(STAGING_BARANGS_DIR / 'PERP-PROJ.csv', index=False)
pd.DataFrame(sub_lots_proj).to_csv(STAGING_LOTS_DIR / 'PERP-PROJ.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_proj_u.columns: df_proj_u[c] = pd.to_numeric(df_proj_u[c], errors='coerce').astype('Int64')
df_proj_u.to_csv(STAGING_UNITS_DIR / 'PERP-PROJ.csv', index=False)

# --- 2. PERP-RAKS ---
df_raks_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-RAKS.csv')
TARGET_RAKS = [
    ('86', 'Rak Switch/Hub (50 cm)', 'Tinggi 50 cm', [2642]),
    ('66', 'Rak Server (2 m)', 'Tinggi 2 m', [2980]),
    ('66', 'Closed Rack 42U', '19" Depth 1100 mm', [3960, 3961, 3962]),
    ('86', 'Rak Server', None, [6519])
]
sub_barangs_raks = []
sub_lots_raks = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_RAKS, start=1):
    bnum = f'PERP-RAKS-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_raks.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-RAKS'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_raks.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_raks_u[df_raks_u['ams_asset_id'].isin(aids)].index:
        df_raks_u.at[idx, 'lot_id'] = seq
        df_raks_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_raks).to_csv(STAGING_BARANGS_DIR / 'PERP-RAKS.csv', index=False)
pd.DataFrame(sub_lots_raks).to_csv(STAGING_LOTS_DIR / 'PERP-RAKS.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_raks_u.columns: df_raks_u[c] = pd.to_numeric(df_raks_u[c], errors='coerce').astype('Int64')
df_raks_u.to_csv(STAGING_UNITS_DIR / 'PERP-RAKS.csv', index=False)

# --- 3. PERP-SCAN ---
df_scan_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-SCAN.csv')
TARGET_SCAN = [
    ('8', 'Scanner A3 Mono', None, [2624]),
    ('9', 'Scanner A4 Color', None, [2639, 2640]),
    ('17', 'Scanner A4 Color', None, [3004]),
    ('17', 'CanoScan LiDE', 'A4 Color', [3068]),
    ('17', 'imageFORMULA DR-6030C', 'A3 Color Duplex', [3430]),
    ('9', 'CanoScan LiDE 110', 'A4 Color', [3781]),
    ('8', 'fi-7480', 'ADF / Duplex A3 Scanner, 80 ppm', [8087, 8100])
]
sub_barangs_scan = []
sub_lots_scan = []
for seq, (b_id, name, spec, aids) in enumerate(TARGET_SCAN, start=1):
    bnum = f'PERP-SCAN-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_scan.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-SCAN'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_scan.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_scan_u[df_scan_u['ams_asset_id'].isin(aids)].index:
        df_scan_u.at[idx, 'lot_id'] = seq
        df_scan_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_scan).to_csv(STAGING_BARANGS_DIR / 'PERP-SCAN.csv', index=False)
pd.DataFrame(sub_lots_scan).to_csv(STAGING_LOTS_DIR / 'PERP-SCAN.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_scan_u.columns: df_scan_u[c] = pd.to_numeric(df_scan_u[c], errors='coerce').astype('Int64')
df_scan_u.to_csv(STAGING_UNITS_DIR / 'PERP-SCAN.csv', index=False)

# --- 4. PERP-SCRN ---
df_scrn_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-SCRN.csv')
sub_barangs_scrn = [{
    'id': 1, 'number': 'PERP-SCRN-0001', 'subcategory_id': sub_map['PERP-SCRN'],
    'brand_id': '39', 'uom_id': 1, 'name': 'Screen Presentation', 'specification': 'Standing Portable',
    'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
    'created_at': now_str, 'updated_at': now_str
}]
sub_lots_scrn = [{
    'id': 1, 'number': 'LOT-0001-26-PERP-SCRN-0001', 'barang_id': 1, 'organizer_id': 1,
    'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
    'initial_quantity': None, 'current_quantity': None, 'po_number': None,
    'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
    'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
}]
pd.DataFrame(sub_barangs_scrn).to_csv(STAGING_BARANGS_DIR / 'PERP-SCRN.csv', index=False)
pd.DataFrame(sub_lots_scrn).to_csv(STAGING_LOTS_DIR / 'PERP-SCRN.csv', index=False)
df_scrn_u.at[0, 'lot_id'] = 1
df_scrn_u.at[0, 'specification'] = 'Standing Portable'
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_scrn_u.columns: df_scrn_u[c] = pd.to_numeric(df_scrn_u[c], errors='coerce').astype('Int64')
df_scrn_u.to_csv(STAGING_UNITS_DIR / 'PERP-SCRN.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(sub_barangs_proj) == 10 and len(df_proj_u) == 16
assert len(sub_barangs_raks) == 4 and len(df_raks_u) == 6
assert len(sub_barangs_scan) == 7 and len(df_scan_u) == 9
assert len(sub_barangs_scrn) == 1 and len(df_scrn_u) == 1
print(f"\\n[SUCCESS] Standardized PROJ (10), RAKS (4), SCAN (7), SCRN (1).")
""")

# -----------------------------------------------------------------------------
# Section 62: PERP-STRG
# -----------------------------------------------------------------------------
s62_md = make_md_cell('cell_s62_md', """---
## 62. Subcategory PERP-STRG Consolidation
### Internal Enterprise Server HDDs & High-Capacity External Drives

- Distinguishes enterprise data storage drives from removable external media (`PERP-MEXT`).
- Consolidates 15 legacy barangs down to 13 master barangs across 19 units.
- Merges 3 redundant SanDisk Extreme Portable SSD 2TB entries.
""")

s62_code = make_code_cell('cell_s62_code', """# =============================================================================
# 62. PERP-STRG Consolidation
# =============================================================================
print(f"\\n{'='*80}")
print("Consolidating PERP-STRG")
print(f"{'='*80}\\n")

df_strg_u = pd.read_csv(STAGING_UNITS_DIR / 'PERP-STRG.csv')

TARGET_STRG = [
    ('85', 'HDD WD Red Plus 12TB', '3.5" SATA 7200 RPM', [7929, 7930]), # 0001
    ('29', 'SSD External 1TB', None, [8047, 8119]), # 0002
    ('29', 'SSD External 500GB', None, [8048]), # 0003
    ('29', 'SSD External 2TB', None, [8073]), # 0004
    ('84', 'HDD External 1TB', 'One Touch USB 3.0', [8145, 8146]), # 0005
    ('147', 'Extreme Portable SSD 2TB', 'USB 3.2 Gen 2', [10520, 10521, 10522, 10523]), # Merged 0006, 0007, 0008
    ('85', 'SSD External 1TB', 'Elements SE', [10565]), # 0009
    ('85', 'HDD External 8TB', 'My Book Desktop', [10572]), # 0010
    ('84', 'HDD Enterprise 16TB', 'Exos X18 SATA 7200 RPM', [11858]), # 0011
    ('84', 'HDD Enterprise 10TB', 'Exos X18 SATA 7200 RPM', [11859]), # 0012
    ('84', 'HDD Enterprise 8TB', 'Exos 7E10 SATA 7200 RPM', [11860]), # 0013
    ('84', 'HDD Enterprise 4TB', 'Exos 7E10 SATA 7200 RPM', [11875]), # 0014
    ('84', 'HDD Enterprise 30TB', 'Exos ST30000NM004K SATA', [11948]) # 0015
]

sub_barangs_strg = []
sub_lots_strg = []

for seq, (b_id, name, spec, aids) in enumerate(TARGET_STRG, start=1):
    bnum = f'PERP-STRG-{seq:04d}'
    lnum = f'LOT-0001-26-{bnum}'
    sub_barangs_strg.append({
        'id': seq, 'number': bnum, 'subcategory_id': sub_map['PERP-STRG'],
        'brand_id': b_id, 'uom_id': 1, 'name': name, 'specification': spec,
        'min_stock_threshold': None, 'image_url': None, 'last_restock_at': None,
        'created_at': now_str, 'updated_at': now_str
    })
    sub_lots_strg.append({
        'id': seq, 'number': lnum, 'barang_id': seq, 'organizer_id': 1,
        'vendor_id': None, 'legacy_vendor_id': None, 'location_id': None,
        'initial_quantity': None, 'current_quantity': None, 'po_number': None,
        'date_of_receipt': now_str, 'unit_price': None, 'image_url': None,
        'burden': None, 'project_id': None, 'created_at': now_str, 'updated_at': now_str
    })
    for idx in df_strg_u[df_strg_u['ams_asset_id'].isin(aids)].index:
        df_strg_u.at[idx, 'lot_id'] = seq
        df_strg_u.at[idx, 'specification'] = spec

pd.DataFrame(sub_barangs_strg).to_csv(STAGING_BARANGS_DIR / 'PERP-STRG.csv', index=False)
pd.DataFrame(sub_lots_strg).to_csv(STAGING_LOTS_DIR / 'PERP-STRG.csv', index=False)
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_strg_u.columns: df_strg_u[c] = pd.to_numeric(df_strg_u[c], errors='coerce').astype('Int64')
df_strg_u.to_csv(STAGING_UNITS_DIR / 'PERP-STRG.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(sub_barangs_strg) == 13, f"Expected 13 STRG barangs, got {len(sub_barangs_strg)}"
assert len(df_strg_u) == 19, f"Expected 19 STRG units, got {len(df_strg_u)}"
print(f"\\n[SUCCESS] Consolidated PERP-STRG from 15 down to {len(sub_barangs_strg)} barangs across {len(df_strg_u)} units.")
""")

# -----------------------------------------------------------------------------
# Section 63: Verification & Global Integrity Check
# -----------------------------------------------------------------------------
s63_md = make_md_cell('cell_s63_md', """---
## 63. Peripheral Batch Verification & Global Integrity Check
### Quality Assertions Across All PERP Subcategories, ELEK-FR, and Master Deliverables
Validates that units are strictly 6,939, master barangs are strictly 669, and SQL scripts are in sync.
""")

s63_code = make_code_cell('cell_s63_code', """# =============================================================================
# 63. Peripheral Batch Quality Assertions & Global Master Integrity
# =============================================================================
print(f"\\n{'='*80}")
print("Verifying Peripheral Batch Masters (PERP & ELEK-FR) & Global Consistency")
print(f"{'='*80}\\n")

# 1. Partition Assertions
expected_batch_units = {
    'PERP-ACCN': 3,
    'ELEK-FR': 7,
    'PERP-ACCS': 3,
    'PERP-CAM': 10,
    'PERP-COMM': 16,
    'PERP-MEXT': 24,
    'PERP-MMD': 6,
    'PERP-NETW': 86,
    'PERP-PROJ': 16,
    'PERP-RAKS': 6,
    'PERP-SCAN': 9,
    'PERP-SCRN': 1,
    'PERP-STRG': 19
}
expected_batch_barangs = {
    'PERP-ACCN': 1,
    'ELEK-FR': 3,
    'PERP-ACCS': 3,
    'PERP-CAM': 9,
    'PERP-COMM': 4,
    'PERP-MEXT': 16,
    'PERP-MMD': 5,
    'PERP-NETW': 25,
    'PERP-PROJ': 10,
    'PERP-RAKS': 4,
    'PERP-SCAN': 7,
    'PERP-SCRN': 1,
    'PERP-STRG': 13
}

for sub_c, exp_u in expected_batch_units.items():
    df_u_part = pd.read_csv(STAGING_UNITS_DIR / f'{sub_c}.csv')
    df_b_part = pd.read_csv(STAGING_BARANGS_DIR / f'{sub_c}.csv')
    df_l_part = pd.read_csv(STAGING_LOTS_DIR / f'{sub_c}.csv')
    
    exp_b = expected_batch_barangs[sub_c]
    assert len(df_u_part) == exp_u, f"Mismatch in {sub_c} units: expected {exp_u}, got {len(df_u_part)}"
    assert len(df_b_part) == exp_b, f"Mismatch in {sub_c} barangs: expected {exp_b}, got {len(df_b_part)}"
    assert len(df_l_part) == exp_b, f"Mismatch in {sub_c} lots: expected {exp_b}, got {len(df_l_part)}"
    assert df_u_part['lot_id'].isin(df_l_part['id']).all(), f"Invalid lot_id found in {sub_c} units!"

# 2. Global Master Tables
df_barangs_m = pd.read_csv(FINAL_BARANG_DIR / 'barangs.csv')
df_lots_m = pd.read_csv(FINAL_LOT_DIR / 'lots.csv')
df_units_m = pd.read_csv(FINAL_UNIT_DIR / 'units.csv')

assert len(df_units_m) == 6939, f'Expected 6,939 units, got {len(df_units_m)}'
assert len(df_barangs_m) == len(df_lots_m) == 669, f'Expected 669 barangs & lots, got {len(df_barangs_m)}'
assert (df_barangs_m['id'].astype(int) == list(range(1, len(df_barangs_m) + 1))).all()
assert (df_lots_m['id'].astype(int) == list(range(1, len(df_lots_m) + 1))).all()
assert df_barangs_m['number'].is_unique
assert df_lots_m['number'].is_unique

print(f"[SUCCESS] All assertions passed! Master barangs: {len(df_barangs_m):,}, lots: {len(df_lots_m):,}, units: {len(df_units_m):,}.")
""")

# Replace the last 14 cells (sections 57 to 63)
# Find where Section 57 starts
s57_idx = None
for i, cell in enumerate(nb['cells']):
    if cell.get('id') == 'cell_s57_md':
        s57_idx = i
        break

if s57_idx is not None:
    nb['cells'] = nb['cells'][:s57_idx]

# Append updated cells
nb['cells'].extend([
    s57_md, s57_code,
    s58_md, s58_code,
    s59_md, s59_code,
    s60_md, s60_code,
    s61_md, s61_code,
    s62_md, s62_code,
    s63_md, s63_code
])

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('Updated notebook with verified asset IDs for sections 57 through 63!')
