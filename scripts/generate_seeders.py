import csv
import os
import shutil
from pathlib import Path

def clean_date(d):
    if not d:
        return None
    d = d.strip()
    if d.endswith('.000'):
        d = d[:-4]
    return d

def php_val(val, val_type):
    if val is None or str(val).strip() in ('', 'None', 'nan', 'NULL'):
        return 'null'
    val_str = str(val).strip()
    if val_type == 'int':
        try:
            return str(int(float(val_str)))
        except:
            return 'null'
    elif val_type == 'float':
        try:
            f = float(val_str)
            return str(int(f)) if f.is_integer() else str(f)
        except:
            return 'null'
    elif val_type == 'bool':
        return 'true' if val_str.lower() in ['true', '1'] else 'false'
    elif val_type == 'date':
        cd = clean_date(val_str)
        if not cd:
            return 'null'
        return f"'{cd}'"
    else:
        escaped = val_str.replace('\\', '\\\\').replace("'", "\\'")
        return f"'{escaped}'"

SECTIONS_TO_WRITE = {}

# 1. GENERATE ActualTypeSeeder.php
print("Generating ActualTypeSeeder.php...")
with open('data/smart/final/type/types.csv', encoding='utf-8') as f:
    types = list(csv.DictReader(f))

type_entries = []
for r in types:
    fields = [
        f"'id' => {php_val(r['id'], 'int')}",
        f"'code' => {php_val(r['code'], 'str')}",
        f"'name' => {php_val(r['name'], 'str')}",
        f"'description' => {php_val(r['description'], 'str')}",
        f"'is_consumable' => {php_val(r['is_consumable'], 'bool')}",
        f"'category_id' => {php_val(r['category_id'], 'int')}",
        f"'created_at' => {php_val(r['created_at'], 'date')}",
        f"'updated_at' => {php_val(r['updated_at'], 'date')}",
    ]
    type_entries.append('            [\n' + ',\n'.join(f'                {f}' for f in fields) + ',\n            ],')

type_content = f'''<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualTypeSeeder extends Seeder
{{
    /**
     * Run the actual Type database seeds.
     * Total records: {len(types)}
     */
    public function run(): void
    {{
        $records = [
{chr(10).join(type_entries)}
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT types ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('types')->upsert(
                $chunk,
                ['id'],
                [
                    'code',
                    'name',
                    'description',
                    'is_consumable',
                    'category_id',
                    'updated_at',
                ]
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT types OFF;');
        }}
    }}
}}
'''
SECTIONS_TO_WRITE['ActualTypeSeeder.php'] = type_content

# 2. GENERATE ActualModelSeeder.php
print("Generating ActualModelSeeder.php...")
with open('data/smart/final/model/models.csv', encoding='utf-8') as f:
    models = list(csv.DictReader(f))

model_entries = []
for r in models:
    fields = [
        f"'id' => {php_val(r['id'], 'int')}",
        f"'number' => {php_val(r['number'], 'str')}",
        f"'type_id' => {php_val(r['type_id'], 'int')}",
        f"'brand_id' => {php_val(r['brand_id'], 'int')}",
        f"'uom_id' => {php_val(r['uom_id'], 'int')}",
        f"'name' => {php_val(r['name'], 'str')}",
        f"'specification' => {php_val(r['specification'], 'str')}",
        f"'min_stock_threshold' => {php_val(r['min_stock_threshold'], 'int')}",
        f"'last_restock_at' => {php_val(r['last_restock_at'], 'date')}",
        f"'created_at' => {php_val(r['created_at'], 'date')}",
        f"'updated_at' => {php_val(r['updated_at'], 'date')}",
    ]
    model_entries.append('            [\n' + ',\n'.join(f'                {f}' for f in fields) + ',\n            ],')

model_content = f'''<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualModelSeeder extends Seeder
{{
    /**
     * Run the actual Model database seeds.
     * Total records: {len(models)}
     */
    public function run(): void
    {{
        $records = [
{chr(10).join(model_entries)}
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT models ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('models')->upsert(
                $chunk,
                ['id'],
                [
                    'number',
                    'type_id',
                    'brand_id',
                    'uom_id',
                    'name',
                    'specification',
                    'min_stock_threshold',
                    'last_restock_at',
                    'updated_at',
                ]
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT models OFF;');
        }}
    }}
}}
'''
SECTIONS_TO_WRITE['ActualModelSeeder.php'] = model_content

# 3. GENERATE ActualLotSeeder.php
print("Generating ActualLotSeeder.php...")
with open('data/smart/final/lot/lots.csv', encoding='utf-8') as f:
    lots = list(csv.DictReader(f))

lot_entries = []
for r in lots:
    fields = [
        f"'id' => {php_val(r['id'], 'int')}",
        f"'number' => {php_val(r['number'], 'str')}",
        f"'model_id' => {php_val(r['model_id'], 'int')}",
        f"'organizer_id' => {php_val(r['organizer_id'], 'int')}",
        f"'vendor_id' => {php_val(r['vendor_id'], 'int')}",
        f"'legacy_vendor_id' => {php_val(r['legacy_vendor_id'], 'int')}",
        f"'initial_quantity' => {php_val(r['initial_quantity'], 'int')}",
        f"'current_quantity' => {php_val(r['current_quantity'], 'int')}",
        f"'entry_type' => {php_val(r['entry_type'], 'str')}",
        f"'po_number' => {php_val(r['po_number'], 'str')}",
        f"'purchase_grant_date' => {php_val(r['purchase_grant_date'], 'date')}",
        f"'memo_number' => {php_val(r['memo_number'], 'str')}",
        f"'memo_url' => {php_val(r['memo_url'], 'str')}",
        f"'burden' => {php_val(r['burden'], 'str')}",
        f"'project_id' => {php_val(r['project_id'], 'int')}",
        f"'created_at' => {php_val(r['created_at'], 'date')}",
        f"'updated_at' => {php_val(r['updated_at'], 'date')}",
    ]
    lot_entries.append('            [\n' + ',\n'.join(f'                {f}' for f in fields) + ',\n            ],')

lot_content = f'''<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualLotSeeder extends Seeder
{{
    /**
     * Run the actual Lot database seeds.
     * Total records: {len(lots)}
     */
    public function run(): void
    {{
        $records = [
{chr(10).join(lot_entries)}
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT lots ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('lots')->upsert(
                $chunk,
                ['id'],
                [
                    'number',
                    'model_id',
                    'organizer_id',
                    'vendor_id',
                    'legacy_vendor_id',
                    'initial_quantity',
                    'current_quantity',
                    'entry_type',
                    'po_number',
                    'purchase_grant_date',
                    'memo_number',
                    'memo_url',
                    'burden',
                    'project_id',
                    'updated_at',
                ]
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT lots OFF;');
        }}
    }}
}}
'''
SECTIONS_TO_WRITE['ActualLotSeeder.php'] = lot_content

# 4. GENERATE ActualAssetSeeder.php
print("Generating ActualAssetSeeder.php...")
with open('data/smart/final/asset/assets.csv', encoding='utf-8') as f:
    assets = list(csv.DictReader(f))

asset_entries = []
for r in assets:
    fields = [
        f"'id' => {php_val(r['id'], 'int')}",
        f"'number' => {php_val(r['number'], 'str')}",
        f"'legacy_number' => {php_val(r['legacy_number'], 'str')}",
        f"'lot_id' => {php_val(r['lot_id'], 'int')}",
        f"'legacy_vendor_id' => {php_val(r['legacy_vendor_id'], 'int')}",
        f"'location_id' => {php_val(r['location_id'], 'int')}",
        f"'status' => {php_val(r['status'], 'str')}",
        f"'condition' => {php_val(r['condition'], 'str')}",
        f"'comp_specification' => {php_val(r['comp_specification'], 'str')}",
        f"'borrowing_type' => {php_val(r['borrowing_type'], 'str')}",
        f"'classification' => {php_val(r['classification'], 'str')}",
        f"'price' => {php_val(r['price'], 'float')}",
        f"'image_url' => {php_val(r['image_url'], 'str')}",
        f"'vehicle_registration' => {php_val(r['vehicle_registration'], 'str')}",
        f"'legacy_burden' => {php_val(r['legacy_burden'], 'str')}",
        f"'legacy_project_id' => {php_val(r['legacy_project_id'], 'int')}",
        f"'created_at' => {php_val(r['created_at'], 'date')}",
        f"'updated_at' => {php_val(r['updated_at'], 'date')}",
    ]
    asset_entries.append('            [' + ', '.join(fields) + '],')

asset_content = f'''<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualAssetSeeder extends Seeder
{{
    /**
     * Run the actual Asset database seeds.
     * Total records: {len(assets)}
     */
    public function run(): void
    {{
        $records = [
{chr(10).join(asset_entries)}
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT assets ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('assets')->upsert(
                $chunk,
                ['id'],
                [
                    'number',
                    'legacy_number',
                    'lot_id',
                    'legacy_vendor_id',
                    'location_id',
                    'status',
                    'condition',
                    'comp_specification',
                    'borrowing_type',
                    'classification',
                    'price',
                    'image_url',
                    'vehicle_registration',
                    'legacy_burden',
                    'legacy_project_id',
                    'updated_at',
                ]
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT assets OFF;');
        }}
    }}
}}
'''
SECTIONS_TO_WRITE['ActualAssetSeeder.php'] = asset_content

# Write to ams-smart-migration and smart repo
out_dirs = [
    Path('database/seeders'),
    Path('/home/ran/Devs/smart/database/seeders')
]

for filename, content in SECTIONS_TO_WRITE.items():
    for target_dir in out_dirs:
        if target_dir.exists():
            target_path = target_dir / filename
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Saved: {target_path}")

# Clean up deprecated seeders if present in ams-smart-migration
deprecated_files = [
    'ActualSubcategorySeeder.php',
    'ActualBarangSeeder.php',
    'ActualUnitSeeder.php'
]
for dep in deprecated_files:
    p = Path('database/seeders') / dep
    if p.exists():
        p.unlink()
        print(f"Removed deprecated seeder: {p}")

print("\nAll seeders generated and synchronized successfully!")
