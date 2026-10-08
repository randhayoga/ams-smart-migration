import csv
import os

def clean_date(d):
    if not d:
        return None
    d = d.strip()
    if d.endswith('.000'):
        d = d[:-4]
    return d

def php_val(val, val_type):
    if val is None or str(val).strip() == '':
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

# 1. GENERATE ActualBarangSeeder.php
with open('data/smart/final/barang/barangs.csv') as f:
    barangs = list(csv.DictReader(f))

barang_entries = []
for r in barangs:
    fields = [
        f"'id' => {php_val(r['id'], 'int')}",
        f"'number' => {php_val(r['number'], 'str')}",
        f"'subcategory_id' => {php_val(r['subcategory_id'], 'int')}",
        f"'brand_id' => {php_val(r['brand_id'], 'int')}",
        f"'uom_id' => {php_val(r['uom_id'], 'int')}",
        f"'name' => {php_val(r['name'], 'str')}",
        f"'specification' => {php_val(r['specification'], 'str')}",
        f"'min_stock_threshold' => {php_val(r['min_stock_threshold'], 'int')}",
        f"'image_url' => {php_val(r['image_url'], 'str')}",
        f"'last_restock_at' => {php_val(r['last_restock_at'], 'date')}",
        f"'created_at' => {php_val(r['created_at'], 'date')}",
        f"'updated_at' => {php_val(r['updated_at'], 'date')}",
    ]
    barang_entries.append('            [\n' + ',\n'.join(f'                {f}' for f in fields) + ',\n            ],')

barang_content = f'''<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualBarangSeeder extends Seeder
{{
    /**
     * Run the actual Barang database seeds.
     * Total records: {len(barangs)}
     */
    public function run(): void
    {{
        $records = [
{chr(10).join(barang_entries)}
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT barangs ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('barangs')->upsert(
                $chunk,
                ['id'],
                [
                    'number',
                    'subcategory_id',
                    'brand_id',
                    'uom_id',
                    'name',
                    'specification',
                    'min_stock_threshold',
                    'image_url',
                    'last_restock_at',
                    'updated_at',
                ]
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT barangs OFF;');
        }}
    }}
}}
'''

with open('database/seeders/ActualBarangSeeder.php', 'w') as f:
    f.write(barang_content)
print('ActualBarangSeeder.php generated successfully!')

# 2. GENERATE ActualLotSeeder.php
with open('data/smart/final/lot/lots.csv') as f:
    lots = list(csv.DictReader(f))

lot_entries = []
for r in lots:
    fields = [
        f"'id' => {php_val(r['id'], 'int')}",
        f"'number' => {php_val(r['number'], 'str')}",
        f"'barang_id' => {php_val(r['barang_id'], 'int')}",
        f"'organizer_id' => {php_val(r['organizer_id'], 'int')}",
        f"'vendor_id' => {php_val(r['vendor_id'], 'int')}",
        f"'legacy_vendor_id' => {php_val(r['legacy_vendor_id'], 'int')}",
        f"'location_id' => {php_val(r['location_id'], 'int')}",
        f"'initial_quantity' => {php_val(r['initial_quantity'], 'int')}",
        f"'current_quantity' => {php_val(r['current_quantity'], 'int')}",
        f"'po_number' => {php_val(r['po_number'], 'str')}",
        f"'date_of_receipt' => {php_val(r['date_of_receipt'], 'date')}",
        f"'unit_price' => {php_val(r['unit_price'], 'float')}",
        f"'image_url' => {php_val(r['image_url'], 'str')}",
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
                    'barang_id',
                    'organizer_id',
                    'vendor_id',
                    'legacy_vendor_id',
                    'location_id',
                    'initial_quantity',
                    'current_quantity',
                    'po_number',
                    'date_of_receipt',
                    'unit_price',
                    'image_url',
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

with open('database/seeders/ActualLotSeeder.php', 'w') as f:
    f.write(lot_content)
print('ActualLotSeeder.php generated successfully!')

# 3. GENERATE ActualUnitSeeder.php
with open('data/smart/final/unit/units.csv') as f:
    units = list(csv.DictReader(f))

unit_entries = []
for r in units:
    fields = [
        f"'id' => {php_val(r['id'], 'int')}",
        f"'number' => {php_val(r['number'], 'str')}",
        f"'legacy_number' => {php_val(r['legacy_number'], 'str')}",
        f"'lot_id' => {php_val(r['lot_id'], 'int')}",
        f"'vendor_id' => {php_val(r['vendor_id'], 'int')}",
        f"'location_id' => {php_val(r['location_id'], 'int')}",
        f"'status' => {php_val(r['status'], 'str')}",
        f"'condition' => {php_val(r['condition'], 'str')}",
        f"'specification' => {php_val(r['specification'], 'str')}",
        f"'price' => {php_val(r['price'], 'float')}",
        f"'image_url' => {php_val(r['image_url'], 'str')}",
        f"'vehicle_registration' => {php_val(r['vehicle_registration'], 'str')}",
        f"'burden' => {php_val(r['burden'], 'str')}",
        f"'project_id' => {php_val(r['project_id'], 'int')}",
        f"'type' => {php_val(r['type'], 'str')}",
        f"'classification' => {php_val(r['classification'], 'str')}",
        f"'created_at' => {php_val(r['created_at'], 'date')}",
        f"'updated_at' => {php_val(r['updated_at'], 'date')}",
    ]
    unit_entries.append('            [' + ', '.join(fields) + '],')

unit_content = f'''<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualUnitSeeder extends Seeder
{{
    /**
     * Run the actual Unit database seeds.
     * Total records: {len(units)}
     */
    public function run(): void
    {{
        $records = [
{chr(10).join(unit_entries)}
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT units ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('units')->upsert(
                $chunk,
                ['id'],
                [
                    'number',
                    'legacy_number',
                    'lot_id',
                    'vendor_id',
                    'location_id',
                    'status',
                    'condition',
                    'specification',
                    'price',
                    'image_url',
                    'vehicle_registration',
                    'burden',
                    'project_id',
                    'type',
                    'classification',
                    'updated_at',
                ]
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT units OFF;');
        }}
    }}
}}
'''

with open('database/seeders/ActualUnitSeeder.php', 'w') as f:
    f.write(unit_content)
print('ActualUnitSeeder.php generated successfully!')
