<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class ActualCategorySeeder extends Seeder
{
    /**
     * Run the master Category database seeds.
     * Total records: 13
     */
    public function run(): void
    {
        $records = [
            [
                'id' => 1,
                'code' => 'FUR',
                'name' => 'Furniture',
                'created_at' => '2018-04-05 19:22:48',
                'updated_at' => '2018-04-05 19:22:48',
            ],
            [
                'id' => 2,
                'code' => 'ACC',
                'name' => 'Aksesoris',
                'created_at' => '2016-12-08 14:32:30',
                'updated_at' => '2016-12-08 14:32:30',
            ],
            [
                'id' => 3,
                'code' => 'COMP',
                'name' => 'Computer',
                'created_at' => '2016-12-16 10:11:55',
                'updated_at' => '2016-12-16 10:11:55',
            ],
            [
                'id' => 4,
                'code' => 'MON',
                'name' => 'Monitor',
                'created_at' => '2016-12-16 10:12:31',
                'updated_at' => '2016-12-16 10:12:31',
            ],
            [
                'id' => 5,
                'code' => 'PERP',
                'name' => 'Peripheral',
                'created_at' => '2016-12-16 10:13:22',
                'updated_at' => '2016-12-16 10:13:22',
            ],
            [
                'id' => 6,
                'code' => 'PRNT',
                'name' => 'Printer',
                'created_at' => '2016-12-16 10:14:53',
                'updated_at' => '2016-12-16 10:14:53',
            ],
            [
                'id' => 7,
                'code' => 'SOFT',
                'name' => 'Software',
                'created_at' => '2016-12-16 10:15:22',
                'updated_at' => '2016-12-16 10:15:22',
            ],
            [
                'id' => 8,
                'code' => 'PROP',
                'name' => 'Properti & Gedung',
                'created_at' => '2022-07-01 13:28:04',
                'updated_at' => '2022-07-01 13:28:04',
            ],
            [
                'id' => 9,
                'code' => 'MES',
                'name' => 'Mesin',
                'created_at' => '2017-01-05 17:29:43',
                'updated_at' => '2017-01-05 17:29:43',
            ],
            [
                'id' => 10,
                'code' => 'KEND',
                'name' => 'Kendaraan',
                'created_at' => '2023-06-13 14:02:32',
                'updated_at' => '2023-06-13 14:02:32',
            ],
            [
                'id' => 11,
                'code' => 'ELEK',
                'name' => 'Elektronik',
                'created_at' => '2023-06-13 14:01:35',
                'updated_at' => '2023-06-13 14:01:35',
            ],
            [
                'id' => 12,
                'code' => 'PDGR',
                'name' => 'Pendingin Ruangan',
                'created_at' => '2025-02-05 13:38:52',
                'updated_at' => '2025-02-05 13:38:52',
            ],
            [
                'id' => 13,
                'code' => 'TLKM',
                'name' => 'Telekomunikasi',
                'created_at' => '2025-02-06 10:47:01',
                'updated_at' => '2025-02-06 10:47:01',
            ],
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {
            DB::unprepared('SET IDENTITY_INSERT categories ON;');
        }

        foreach (array_chunk($records, 100) as $chunk) {
            DB::table('categories')->upsert(
                $chunk,
                ['id'],
                ['code', 'name', 'updated_at']
            );
        }

        if ($isSqlsrv) {
            DB::unprepared('SET IDENTITY_INSERT categories OFF;');
        }
    }
}
