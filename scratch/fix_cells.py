import json

with open('notebooks/09_barang_consolidation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 47: ELEK-FR
cell_47_code = """# =============================================================================
# Subcategory ELEK-FR (Fingerprint Reader) Consolidation
# =============================================================================
SUB_CODE = 'ELEK-FR'

print(f"\\n{'='*80}")
print(f"Processing Subcategory: {SUB_CODE}")
print(f"{'='*80}\\n")

df_fr_assets = pd.read_csv(STAGING_ASSETS_DIR / f'{SUB_CODE}.csv', dtype=str)
df_fr_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_CODE}.csv', dtype=str)

TARGET_ORDER_FR = [
    ('124', 'Fingkey Access', None),
    ('133', 'Fingerprint (Lawas)', None),
    ('133', 'M100', 'Mesin Absensi Sidik Jari, LAN')
]

def map_fr_asset(row):
    brand = str(row.get('brand', '')).upper()
    a_id = str(row.get('id', '')).strip()
    if a_id in ['2978', '2984', '2986']:
        return ('133', 'M100', 'Mesin Absensi Sidik Jari, LAN')
    elif a_id == '8948' or 'SOLUTION' in brand:
        return ('133', 'Fingerprint (Lawas)', None)
    else:
        return ('124', 'Fingkey Access', None)

df_fr_merged = df_fr_assets.merge(
    df_fr_units[['ams_asset_id', 'image_url', 'created_at', 'updated_at']],
    left_on='id',
    right_on='ams_asset_id',
    suffixes=('_asset', '_unit')
)

groups = defaultdict(list)
for _, r in df_fr_merged.iterrows():
    target_key = map_fr_asset(r)
    groups[target_key].append(r)

sub_barangs = []
sub_lots = []
unit_lot_map = {}
seq_counter = 1
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.000')

for (b_id, name_val, spec_val) in TARGET_ORDER_FR:
    group_rows = groups.get((b_id, name_val, spec_val), [])
    if not group_rows:
        continue
        
    barang_num = f'{SUB_CODE}-{seq_counter:04d}'
    lot_num = f'LOT-0001-26-{barang_num}'
    
    first_img = None
    for r in group_rows:
        img = r.get('image_url') or r.get('image_url_unit')
        if pd.notna(img) and str(img).strip():
            first_img = str(img).strip()
            break
            
    created_ats = [str(r.get('created_at') or r.get('created_at_unit')) for r in group_rows if pd.notna(r.get('created_at') or r.get('created_at_unit')) and str(r.get('created_at') or r.get('created_at_unit')).strip()]
    updated_ats = [str(r.get('updated_at') or r.get('updated_at_unit')) for r in group_rows if pd.notna(r.get('updated_at') or r.get('updated_at_unit')) and str(r.get('updated_at') or r.get('updated_at_unit')).strip()]
    
    oldest_created = min(created_ats) if created_ats else now_str
    newest_updated = max(updated_ats) if updated_ats else now_str
    org_id = resolve_organizer_id(group_rows[0].get('organizer'))
    
    b_dict = {
        'id': seq_counter,
        'number': barang_num,
        'subcategory_id': sub_map[SUB_CODE],
        'brand_id': b_id,
        'uom_id': 1,
        'name': name_val,
        'specification': spec_val,
        'min_stock_threshold': None,
        'image_url': first_img,
        'last_restock_at': None,
        'created_at': oldest_created,
        'updated_at': newest_updated
    }
    
    l_dict = {
        'id': seq_counter,
        'number': lot_num,
        'barang_id': seq_counter,
        'organizer_id': int(org_id),
        'vendor_id': None,
        'legacy_vendor_id': None,
        'location_id': None,
        'initial_quantity': None,
        'current_quantity': None,
        'po_number': None,
        'date_of_receipt': now_str,
        'unit_price': None,
        'image_url': first_img,
        'burden': None,
        'project_id': None,
        'created_at': now_str,
        'updated_at': now_str
    }
    
    sub_barangs.append(b_dict)
    sub_lots.append(l_dict)
    
    for r in group_rows:
        aid = str(r['id']).strip()
        unit_lot_map[aid] = seq_counter
        
    seq_counter += 1

df_sub_barangs = pd.DataFrame(sub_barangs)
df_sub_lots = pd.DataFrame(sub_lots)

df_sub_barangs.to_csv(STAGING_BARANGS_DIR / f'{SUB_CODE}.csv', index=False)
df_sub_lots.to_csv(STAGING_LOTS_DIR / f'{SUB_CODE}.csv', index=False)

for idx in df_fr_units.index:
    ams_id = str(df_fr_units.at[idx, 'ams_asset_id']).strip()
    if ams_id in unit_lot_map:
        df_fr_units.at[idx, 'lot_id'] = unit_lot_map[ams_id]
    if ams_id in ['2978', '2984', '2986']:
        df_fr_units.at[idx, 'specification'] = 'Mesin Absensi Sidik Jari, LAN'
    else:
        df_fr_units.at[idx, 'specification'] = None

for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_fr_units.columns:
        df_fr_units[c] = pd.to_numeric(df_fr_units[c], errors='coerce').astype('Int64')
df_fr_units.to_csv(STAGING_UNITS_DIR / f'{SUB_CODE}.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(df_sub_barangs) == 3, f'Expected 3 barangs, got {len(df_sub_barangs)}'
assert len(df_fr_units) == 7, f'Expected 7 units, got {len(df_fr_units)}'
print(f"\\n[SUCCESS] Consolidated ELEK-FR to {len(df_sub_barangs)} barangs across 7 units.")
"""

nb['cells'][47]['source'] = [line + '\n' for line in cell_47_code.splitlines()]

# Cell 53: ELEK range assertion
cell_53_src = ''.join(nb['cells'][53]['source'])
cell_53_src = cell_53_src.replace("assert len(pd.read_csv(STAGING_BARANGS_DIR / 'ELEK-FR.csv')) == 2", "assert len(pd.read_csv(STAGING_BARANGS_DIR / 'ELEK-FR.csv')) == 3")
cell_53_src = cell_53_src.replace("assert len(pd.read_csv(STAGING_UNITS_DIR / 'ELEK-FR.csv')) == 4", "assert len(pd.read_csv(STAGING_UNITS_DIR / 'ELEK-FR.csv')) == 7")
nb['cells'][53]['source'] = [line + '\n' for line in cell_53_src.splitlines()]

# Cell 75: ELEK category assertion
cell_75_src = ''.join(nb['cells'][75]['source'])
cell_75_src = cell_75_src.replace("'ELEK-FR': 4,", "'ELEK-FR': 7,")
nb['cells'][75]['source'] = [line + '\n' for line in cell_75_src.splitlines()]

# Cell 114: Section 57 Markdown
cell_114_md = """---
## 57. Subcategory PERP-ACCN Consolidation
### Access Control Typo Correction & Master Alignment

- Biometric fingerprint readers (Solution M100, assets 2978, 2984, 2986) were correctly relocated into `ELEK-FR` (`ELEK-FR-0003`).
- Corrects typo in `PERP-ACCN-0001` specification (`MAKNETIK` -> `Magnetik`).
- `PERP-ACCN`: 1 master barang across 3 units.
- `ELEK-FR`: 3 master barangs across 7 units.
"""
nb['cells'][114]['source'] = [line + '\n' for line in cell_114_md.splitlines()]

# Cell 115: Section 57 Code
cell_115_code = """# =============================================================================
# 57. PERP-ACCN Consolidation
# =============================================================================
SUB_CODE = 'PERP-ACCN'
print(f"\\n{'='*80}")
print(f"Processing Subcategory: {SUB_CODE}")
print(f"{'='*80}\\n")

df_accn_assets = pd.read_csv(STAGING_ASSETS_DIR / f'{SUB_CODE}.csv', dtype=str)
df_accn_units = pd.read_csv(STAGING_UNITS_DIR / f'{SUB_CODE}.csv', dtype=str)

# Correct typo in specification: 'MAKNETIK' -> 'Magnetik'
# CGI (Brand 26), Name: 'Accessnetic', Spec: 'Mesin Akses Kontrol Magnetik'
TARGET_ACCN = [
    ('26', 'Accessnetic', 'Mesin Akses Kontrol Magnetik')
]

sub_barangs = []
sub_lots = []
seq_counter = 1
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S.000')

barang_num = f'{SUB_CODE}-{seq_counter:04d}'
lot_num = f'LOT-0001-26-{barang_num}'

b_dict = {
    'id': seq_counter,
    'number': barang_num,
    'subcategory_id': sub_map[SUB_CODE],
    'brand_id': '26',
    'uom_id': 1,
    'name': 'Accessnetic',
    'specification': 'Mesin Akses Kontrol Magnetik',
    'min_stock_threshold': None,
    'image_url': None,
    'last_restock_at': None,
    'created_at': '2017-01-04 00:00:00.000',
    'updated_at': '2017-01-04 00:00:00.000'
}

l_dict = {
    'id': seq_counter,
    'number': lot_num,
    'barang_id': seq_counter,
    'organizer_id': 1,
    'vendor_id': None,
    'legacy_vendor_id': None,
    'location_id': None,
    'initial_quantity': None,
    'current_quantity': None,
    'po_number': None,
    'date_of_receipt': now_str,
    'unit_price': None,
    'image_url': None,
    'burden': None,
    'project_id': None,
    'created_at': now_str,
    'updated_at': now_str
}

sub_barangs.append(b_dict)
sub_lots.append(l_dict)

df_sub_barangs = pd.DataFrame(sub_barangs)
df_sub_lots = pd.DataFrame(sub_lots)

df_sub_barangs.to_csv(STAGING_BARANGS_DIR / f'{SUB_CODE}.csv', index=False)
df_sub_lots.to_csv(STAGING_LOTS_DIR / f'{SUB_CODE}.csv', index=False)

df_accn_units['lot_id'] = 1
df_accn_units['specification'] = 'Mesin Akses Kontrol Magnetik'
for c in ['id', 'lot_id', 'location_id', 'project_id', 'vendor_id']:
    if c in df_accn_units.columns:
        df_accn_units[c] = pd.to_numeric(df_accn_units[c], errors='coerce').astype('Int64')
df_accn_units.to_csv(STAGING_UNITS_DIR / f'{SUB_CODE}.csv', index=False)

df_all_barangs, df_all_lots, df_all_units = sync_consolidated_masters()

assert len(df_sub_barangs) == 1, f'Expected 1 barang, got {len(df_sub_barangs)}'
assert len(df_accn_units) == 3, f'Expected 3 units, got {len(df_accn_units)}'
assert len(pd.read_csv(STAGING_BARANGS_DIR / 'ELEK-FR.csv')) == 3, 'Expected 3 barangs in ELEK-FR'
assert len(pd.read_csv(STAGING_UNITS_DIR / 'ELEK-FR.csv')) == 7, 'Expected 7 units in ELEK-FR'
print(f"\\n[SUCCESS] Consolidated PERP-ACCN to 1 barang across 3 units; verified ELEK-FR 3 barangs across 7 units.")
"""
nb['cells'][115]['source'] = [line + '\n' for line in cell_115_code.splitlines()]

# Cell 127: Final assertion
cell_127_code = """# =============================================================================
# 63. Peripheral Batch Verification & Global Integrity Check
# =============================================================================
print(f"\\n{'='*80}")
print("Verifying Peripheral Batch Masters & System-Wide Invariants")
print(f"{'='*80}\\n")

expected_units_batch = {
    'PERP-ACCN': 3,
    'PERP-ACCS': 25,
    'PERP-CAM': 16,
    'PERP-COMM': 1,
    'PERP-MEXT': 24,
    'PERP-MMD': 6,
    'PERP-NETW': 86,
    'PERP-PROJ': 13,
    'PERP-RAKS': 3,
    'PERP-SCAN': 8,
    'PERP-SCRN': 10,
    'PERP-STRG': 19,
    'ELEK-FR': 7
}

for sub_c, exp_count in expected_units_batch.items():
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

assert len(df_barangs_m) == 669, f"Expected 669 barangs, got {len(df_barangs_m)}"
assert len(df_lots_m) == 669, f"Expected 669 lots, got {len(df_lots_m)}"
assert len(df_units_m) == 6939, f"Expected 6,939 units, got {len(df_units_m)}"

assert (df_barangs_m['id'].astype(int) == list(range(1, len(df_barangs_m) + 1))).all()
assert (df_lots_m['id'].astype(int) == list(range(1, len(df_lots_m) + 1))).all()
assert df_barangs_m['number'].is_unique
assert df_lots_m['number'].is_unique

print(f"[SUCCESS] All Peripheral batch and system-wide assertions passed successfully!")
print(f"Master barangs: {len(df_barangs_m):,}")
print(f"Master lots:    {len(df_lots_m):,}")
print(f"Master units:   {len(df_units_m):,}")
"""
nb['cells'][127]['source'] = [line + '\n' for line in cell_127_code.splitlines()]

with open('notebooks/09_barang_consolidation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('Updated cells 47, 53, 75, 114, 115, 127 cleanly and successfully!')
