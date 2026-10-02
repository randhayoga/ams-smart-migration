#!/usr/bin/env python3
"""
Convert cleaned master data from data/smart/final/*.csv into Laravel seeders.
Supports writing to ams-smart-migration/database/seeders/ and syncing to SMART.
"""

import argparse
import csv
import os
import shutil
import sys
from pathlib import Path


def sanitize_str(val: str) -> str:
    """Trim whitespace and return sanitized string."""
    return val.strip() if val else ""


def normalize_timestamp(val: str) -> str:
    """Normalize 'YYYY-MM-DD HH:MM:SS.000' to 'YYYY-MM-DD HH:MM:SS'."""
    val = sanitize_str(val)
    if not val:
        return "2026-01-01 00:00:00"
    if "." in val:
        val = val.split(".")[0]
    return val


def format_php_val(val) -> str:
    """Format Python value as PHP literal."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, int):
        return str(val)
    if isinstance(val, float):
        if val.is_integer():
            return str(int(val))
        return str(val)

    # String value
    s = str(val)
    # Check if string contains newlines
    if "\n" in s or "\r" in s:
        escaped_double = (
            s.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\r", "")
            .replace("\n", "\\n")
        )
        return f'"{escaped_double}"'

    # Single-quote escaped string
    escaped_single = s.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped_single}'"


def render_array(records, indent_level=3) -> str:
    """Render a list of dictionaries as a formatted PHP array."""
    indent = "    " * indent_level
    inner_indent = "    " * (indent_level + 1)
    lines = []
    lines.append(f"{indent}[")
    for r in records:
        lines.append(f"{inner_indent}[")
        for k, v in r.items():
            php_v = format_php_val(v)
            lines.append(f"{inner_indent}    '{k}' => {php_v},")
        lines.append(f"{inner_indent}],")
    lines.append(f"{indent}]")
    return "\n".join(lines)


def generate_actual_category_seeder(csv_path: Path) -> str:
    records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "id": int(row["id"]),
                "code": sanitize_str(row["code"]).upper(),
                "name": sanitize_str(row["name"]),
                "created_at": normalize_timestamp(row.get("created_at")),
                "updated_at": normalize_timestamp(row.get("updated_at")),
            })

    # Sort by ID
    records.sort(key=lambda x: x["id"])
    array_code = render_array(records, indent_level=2)

    return f"""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualCategorySeeder extends Seeder
{{
    /**
     * Run the master Category database seeds.
     * Total records: {len(records)}
     */
    public function run(): void
    {{
        $records = {array_code.lstrip()};

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT categories ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('categories')->upsert(
                $chunk,
                ['id'],
                ['code', 'name', 'updated_at']
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT categories OFF;');
        }}
    }}
}}
"""


def generate_actual_subcategory_seeder(csv_path: Path) -> str:
    records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = sanitize_str(row.get("description", ""))
            consumable_str = sanitize_str(row.get("is_consumable", "false")).lower()
            is_consumable = consumable_str in ["true", "1", "t"]

            records.append({
                "id": int(row["id"]),
                "code": sanitize_str(row["code"]),
                "name": sanitize_str(row["name"]),
                "description": desc if desc else None,
                "is_consumable": is_consumable,
                "category_id": int(row["category_id"]),
                "created_at": normalize_timestamp(row.get("created_at")),
                "updated_at": normalize_timestamp(row.get("updated_at")),
            })

    records.sort(key=lambda x: x["id"])
    array_code = render_array(records, indent_level=2)

    return f"""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualSubcategorySeeder extends Seeder
{{
    /**
     * Run the master Subcategory database seeds.
     * Total records: {len(records)}
     */
    public function run(): void
    {{
        $records = {array_code.lstrip()};

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT subcategories ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('subcategories')->upsert(
                $chunk,
                ['id'],
                ['code', 'name', 'description', 'is_consumable', 'category_id', 'updated_at']
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT subcategories OFF;');
        }}
    }}
}}
"""


def generate_actual_brand_seeder(csv_path: Path) -> str:
    records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = sanitize_str(row.get("description", ""))
            records.append({
                "id": int(row["id"]),
                "name": sanitize_str(row["name"]),
                "description": desc if desc else None,
                "created_at": normalize_timestamp(row.get("created_at")),
                "updated_at": normalize_timestamp(row.get("updated_at")),
            })

    records.sort(key=lambda x: x["id"])
    array_code = render_array(records, indent_level=2)

    return f"""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualBrandSeeder extends Seeder
{{
    /**
     * Run the master Brand database seeds.
     * Total records: {len(records)}
     */
    public function run(): void
    {{
        $records = {array_code.lstrip()};

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT brands ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('brands')->upsert(
                $chunk,
                ['id'],
                ['name', 'description', 'updated_at']
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT brands OFF;');
        }}
    }}
}}
"""


def generate_actual_vendor_seeder(csv_path: Path) -> str:
    records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            def val_or_null(col):
                v = sanitize_str(row.get(col, ""))
                return v if v else None

            records.append({
                "id": int(row["id"]),
                "code": sanitize_str(row["code"]),
                "name": sanitize_str(row["name"]),
                "address": val_or_null("address"),
                "phone_number": val_or_null("phone_number"),
                "email": val_or_null("email"),
                "description": val_or_null("description"),
                "contact_person_1": val_or_null("contact_person_1"),
                "cp_email_1": val_or_null("cp_email_1"),
                "cp_phone_1": val_or_null("cp_phone_1"),
                "contact_person_2": val_or_null("contact_person_2"),
                "cp_email_2": val_or_null("cp_email_2"),
                "cp_phone_2": val_or_null("cp_phone_2"),
                "created_at": normalize_timestamp(row.get("created_at")),
                "updated_at": normalize_timestamp(row.get("updated_at")),
            })

    records.sort(key=lambda x: x["id"])
    array_code = render_array(records, indent_level=2)

    return f"""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualVendorSeeder extends Seeder
{{
    /**
     * Run the master Vendor database seeds.
     * Total records: {len(records)}
     */
    public function run(): void
    {{
        $records = {array_code.lstrip()};

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT vendors ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('vendors')->upsert(
                $chunk,
                ['id'],
                [
                    'code',
                    'name',
                    'address',
                    'phone_number',
                    'email',
                    'description',
                    'contact_person_1',
                    'cp_email_1',
                    'cp_phone_1',
                    'contact_person_2',
                    'cp_email_2',
                    'cp_phone_2',
                    'updated_at',
                ]
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT vendors OFF;');
        }}
    }}
}}
"""


def generate_actual_location_seeder(csv_path: Path) -> str:
    records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = sanitize_str(row.get("parent_id", ""))
            parent_id = int(float(pid)) if pid else None

            rel_dept = sanitize_str(row.get("related_departement", ""))
            related_dept = int(float(rel_dept)) if rel_dept else None

            active_str = sanitize_str(row.get("is_active", "1"))
            is_active = active_str in ["1", "true", "True"]

            records.append({
                "id": int(float(row["id"])),
                "name": sanitize_str(row["name"]),
                "parent_id": parent_id,
                "related_departement": related_dept,
                "is_active": is_active,
                "created_at": normalize_timestamp(row.get("created_at")),
                "updated_at": normalize_timestamp(row.get("updated_at")),
            })

    # The CSV is already topologically sorted (parents appear before children)
    array_code = render_array(records, indent_level=2)

    return f"""<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class ActualLocationSeeder extends Seeder
{{
    /**
     * Run the master Location database seeds.
     * Ordered topologically to ensure parents are seeded before children.
     * Total records: {len(records)}
     */
    public function run(): void
    {{
        $records = {array_code.lstrip()};

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT locations ON;');
        }}

        foreach (array_chunk($records, 100) as $chunk) {{
            DB::table('locations')->upsert(
                $chunk,
                ['id'],
                ['name', 'parent_id', 'related_departement', 'is_active', 'updated_at']
            );
        }}

        if ($isSqlsrv) {{
            DB::unprepared('SET IDENTITY_INSERT locations OFF;');
        }}
    }}
}}
"""


def generate_actual_master_seeder() -> str:
    return """<?php

namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;

class ActualMasterSeeder extends Seeder
{
    /**
     * Run the actual/final master data seeds in relational dependency order.
     */
    public function run(): void
    {
        $this->call([
            ActualCategorySeeder::class,
            ActualSubcategorySeeder::class,
            ActualBrandSeeder::class,
            ActualVendorSeeder::class,
            ActualLocationSeeder::class,
        ]);
    }
}
"""


def generate_dummy_uom_seeder() -> str:
    return """<?php

namespace Database\\Seeders;

use App\\Models\\Master\\Uom;
use Illuminate\\Database\\Seeder;

class DummyUomSeeder extends Seeder
{
    /**
     * Run the UOM master database seeds.
     */
    public function run(): void
    {
        $uoms = ['Unit', 'Rim', 'Buah'];
        foreach ($uoms as $uomName) {
            Uom::firstOrCreate(['name' => $uomName]);
        }
    }
}
"""


def generate_dummy_organizer_seeder() -> str:
    return """<?php

namespace Database\\Seeders;

use App\\Models\\Master\\Organizer;
use Illuminate\\Database\\Seeder;

class DummyOrganizerSeeder extends Seeder
{
    /**
     * Run the Organizer master database seeds.
     */
    public function run(): void
    {
        $organizers = ['CFS', 'ICT', 'HSE'];
        foreach ($organizers as $orgName) {
            Organizer::firstOrCreate(['name' => $orgName]);
        }
    }
}
"""


def generate_dummy_master_seeder() -> str:
    return """<?php

namespace Database\\Seeders;

use App\\Models\\HrdOrgchart;
use App\\Models\\Master\\Brand;
use App\\Models\\Master\\Category;
use App\\Models\\Master\\Location;
use App\\Models\\Master\\Organizer;
use App\\Models\\Master\\Subcategory;
use App\\Models\\Master\\Uom;
use App\\Models\\Master\\Vendor;
use Illuminate\\Database\\Seeder;

class DummyMasterSeeder extends Seeder
{
    /**
     * Run the development dummy master database seeds.
     */
    public function run(): void
    {
        $categories = [
            'ATK' => [
                'name' => 'Alat Tulis Kantor',
            ],
            'FUR' => [
                'name' => 'Furnitur',
            ],
            'COMP' => [
                'name' => 'Computer',
            ],
            'MON' => [
                'name' => 'Monitor',
            ],
            'KEN' => [
                'name' => 'Kendaraan',
            ],
        ];
        $categoryModels = [];
        foreach ($categories as $code => $data) {
            $categoryModels[$code] = Category::firstOrCreate(
                ['code' => $code],
                ['name' => $data['name']]
            );
        }

        $subcategories = [
            [
                'code' => 'ATK-HVS4',
                'name' => 'Kertas HVS A4',
                'category_code' => 'ATK',
                'is_consumable' => true,
            ],
            [
                'code' => 'ATK-PLPH',
                'name' => 'Pulpen Hitam',
                'category_code' => 'ATK',
                'is_consumable' => true,
            ],
            [
                'code' => 'FUR-KK',
                'name' => 'Kursi Kerja',
                'description' => 'Kerja, Kerja, Kerja',
                'category_code' => 'FUR',
                'is_consumable' => false,
            ],
            [
                'code' => 'FUR-MK',
                'name' => 'Meja Kerja',
                'category_code' => 'FUR',
                'is_consumable' => false,
            ],
            [
                'code' => 'COMP-NB',
                'name' => 'Notebook',
                'category_code' => 'COMP',
                'is_consumable' => false,
            ],
            [
                'code' => 'MON-LCD',
                'name' => 'LCD',
                'category_code' => 'MON',
                'is_consumable' => false,
            ],
            [
                'code' => 'KEN-MO',
                'name' => 'Mobil',
                'category_code' => 'KEN',
                'is_consumable' => false,
            ],
        ];
        foreach ($subcategories as $sub) {
            Subcategory::firstOrCreate(
                ['code' => $sub['code']],
                [
                    'name' => $sub['name'],
                    'description' => $sub['description'] ?? null,
                    'category_id' => $categoryModels[$sub['category_code']]->id,
                    'is_consumable' => $sub['is_consumable'] ?? false,
                ]
            );
        }

        $uoms = ['Unit', 'Rim', 'Buah'];
        foreach ($uoms as $uomName) {
            Uom::firstOrCreate(['name' => $uomName]);
        }

        $brands = [
            'HP',
            'Lenovo',
            'Acer',
            'Dell',
            'Sinar Dunia',
            'Paper One',
            'Snowman',
            'Standard',
            'IKEA',
            'Informa',
            'Toyota',
            'BYD',
        ];
        foreach ($brands as $brandName) {
            Brand::firstOrCreate(['name' => $brandName]);
        }

        $organizers = ['CFS', 'ICT', 'HSE'];
        foreach ($organizers as $orgName) {
            Organizer::firstOrCreate(['name' => $orgName]);
        }

        $vendors = [
            'PT Surya Abadi Mandiri',
            'PT Jaya Sentosa Sejahtera',
            'PT Media Pratama Nusantara',
            'PT Mitra Global Solusindo',
            'PT Karya Indah Semesta',
        ];
        $vendorCodes = ['VN0001', 'VN0002', 'VN0003', 'VN0004', 'VN0005'];
        foreach ($vendors as $index => $vendorName) {
            Vendor::firstOrCreate(
                ['code' => $vendorCodes[$index]],
                [
                    'name' => $vendorName,
                    'address' => 'Jl. Jenderal Sudirman No. ' . rand(1, 100) . ', Jakarta',
                    'phone_number' => '08' . rand(5000000, 9999999),
                    'email' => strtolower(str_replace(' ', '', $vendorName)) . '@example.com',
                    'description' => 'Supplier untuk ' . $vendorName,
                    'contact_person_1' => 'Budi Santoso',
                    'cp_email_1' => 'budi.santoso@example.com',
                    'cp_phone_1' => '0812' . rand(10000000, 99999999),
                ]
            );
        }

        // 1: Graha RE 1 (Root)
        $graha = Location::firstOrCreate(
            ['name' => 'Graha RE 1', 'parent_id' => null],
            ['is_active' => true]
        );

        // 2: Lantai Mezzanine (Child of Graha RE 1)
        $mezzanine = Location::firstOrCreate(
            ['name' => 'Lantai Mezzanine', 'parent_id' => $graha->id],
            ['is_active' => true]
        );

        // 3: Ruang IFS Departemen (Child of Lantai Mezzanine)
        $ifsDept = HrdOrgchart::where('org_code', 'IFS')->orWhere('org_code', 'TEST-DEPT')->first() ?? HrdOrgchart::first();
        Location::firstOrCreate(
            ['name' => 'Ruang IFS Departemen', 'parent_id' => $mezzanine->id],
            [
                'related_departement' => $ifsDept?->id,
                'is_active' => true,
            ]
        );

        // 4: Lantai 4 (Child of Graha RE 1)
        $lantai4 = Location::firstOrCreate(
            ['name' => 'Lantai 4', 'parent_id' => $graha->id],
            ['is_active' => true]
        );

        // 5: Ruang Mega Mendung (Child of Lantai 4)
        Location::firstOrCreate(
            ['name' => 'Ruang Mega Mendung', 'parent_id' => $lantai4->id],
            ['is_active' => true]
        );

        // 6: Site A (Root)
        Location::firstOrCreate(
            ['name' => 'Site A', 'parent_id' => null],
            ['is_active' => true]
        );
    }
}
"""



def main():
    parser = argparse.ArgumentParser(description="Generate Laravel Seeders from cleaned master data")
    parser.add_argument(
        "--data-dir",
        default="data/smart/final",
        help="Path to final data directory",
    )
    parser.add_argument(
        "--output-dir",
        default="database/seeders",
        help="Destination directory for generated seeders in this repo",
    )
    parser.add_argument(
        "--copy-to-smart",
        action="store_true",
        help="Copy generated seeders directly to SMART (/home/ran/Devs/smart/database/seeders)",
    )
    parser.add_argument(
        "--smart-dir",
        default="/home/ran/Devs/smart/database/seeders",
        help="Target directory in SMART repo",
    )

    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = (base_dir / args.data_dir).resolve()
    out_dir = (base_dir / args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reading cleaned master data from: {data_dir}")
    print(f"Writing seeders to: {out_dir}")

    files_generated = {}

    # 1. Actual Categories
    cat_csv = data_dir / "category" / "categories.csv"
    files_generated["ActualCategorySeeder.php"] = generate_actual_category_seeder(cat_csv)

    # 2. Actual Subcategories
    sub_csv = data_dir / "subcategory" / "subcategories.csv"
    files_generated["ActualSubcategorySeeder.php"] = generate_actual_subcategory_seeder(sub_csv)

    # 3. Actual Brands
    brand_csv = data_dir / "brand" / "brands.csv"
    files_generated["ActualBrandSeeder.php"] = generate_actual_brand_seeder(brand_csv)

    # 4. Actual Vendors
    vendor_csv = data_dir / "vendor" / "vendors.csv"
    files_generated["ActualVendorSeeder.php"] = generate_actual_vendor_seeder(vendor_csv)

    # 5. Actual Locations
    loc_csv = data_dir / "location" / "locations.csv"
    files_generated["ActualLocationSeeder.php"] = generate_actual_location_seeder(loc_csv)

    # 6. Actual Master Seeder
    files_generated["ActualMasterSeeder.php"] = generate_actual_master_seeder()

    # 7. Dummy UOM Seeder
    files_generated["DummyUomSeeder.php"] = generate_dummy_uom_seeder()

    # 8. Dummy Organizer Seeder
    files_generated["DummyOrganizerSeeder.php"] = generate_dummy_organizer_seeder()

    # 9. Dummy Master Seeder
    files_generated["DummyMasterSeeder.php"] = generate_dummy_master_seeder()

    for filename, content in files_generated.items():
        dest = out_dir / filename
        dest.write_text(content, encoding="utf-8")
        print(f"  ✓ Generated: {dest}")

    # Copy to SMART if requested
    if args.copy_to_smart:
        smart_path = Path(args.smart_dir)
        if not smart_path.exists():
            print(f"Error: SMART seeders path does not exist: {smart_path}", file=sys.stderr)
            sys.exit(1)

        print(f"\nSyncing seeders to SMART: {smart_path}")
        for filename, content in files_generated.items():
            smart_dest = smart_path / filename
            smart_dest.write_text(content, encoding="utf-8")
            print(f"  ✓ Synced to SMART: {smart_dest}")

    print("\nSeeder generation completed successfully!")


if __name__ == "__main__":
    main()
