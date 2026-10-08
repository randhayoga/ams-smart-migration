import json

with open('notebooks/09_barang_consolidation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 127: Final assertion
cell_127_code = r'''# =============================================================================
# 63. Peripheral Batch Verification & Global Integrity Check
# =============================================================================
print("\n" + "=" * 80)
print("Verifying Peripheral Batch Masters & System-Wide Invariants")
print("=" * 80 + "\n")

expected_units_batch = {
    'PERP-ACCN': 3,
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

print("[SUCCESS] All Peripheral batch and system-wide assertions passed successfully!")
print(f"Master barangs: {len(df_barangs_m):,}")
print(f"Master lots:    {len(df_lots_m):,}")
print(f"Master units:   {len(df_units_m):,}")
'''

nb['cells'][127]['source'] = [line + '\n' for line in cell_127_code.splitlines()]

# Also check Cell 47 and Cell 115 prints to make sure they use clean concatenation without raw \n in f-strings:
for idx in range(len(nb['cells'])):
    cell = nb['cells'][idx]
    if cell.get('cell_type') == 'code':
        src = ''.join(cell.get('source', []))
        try:
            compile(src, f'<cell_{idx}>', 'exec')
        except SyntaxError as e:
            print(f"SYNTAX ERROR in cell {idx}: {e}")
            raise

with open('notebooks/09_barang_consolidation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('All 128 cells in notebook compiled and validated with ZERO syntax errors!')
