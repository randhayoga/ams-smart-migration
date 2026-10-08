<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class ActualUomSeeder extends Seeder
{
    /**
     * Run the master UOM database seeds.
     * Total records: 3
     */
    public function run(): void
    {
        $records = [
            [
                'id' => 1,
                'name' => 'Unit',
                'created_at' => '2026-04-27 10:59:38',
                'updated_at' => '2026-04-27 10:59:38',
            ],
            [
                'id' => 2,
                'name' => 'Rim',
                'created_at' => '2026-04-27 10:59:38',
                'updated_at' => '2026-04-27 10:59:38',
            ],
            [
                'id' => 3,
                'name' => 'Buah',
                'created_at' => '2026-04-27 10:59:38',
                'updated_at' => '2026-04-27 10:59:38',
            ],
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {
            DB::unprepared('SET IDENTITY_INSERT uoms ON;');
        }

        foreach (array_chunk($records, 100) as $chunk) {
            DB::table('uoms')->upsert(
                $chunk,
                ['id'],
                ['name', 'updated_at']
            );
        }

        if ($isSqlsrv) {
            DB::unprepared('SET IDENTITY_INSERT uoms OFF;');
        }
    }
}
