<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class ActualOrganizerSeeder extends Seeder
{
    /**
     * Run the master Organizer database seeds.
     * Total records: 3
     */
    public function run(): void
    {
        $records = [
            [
                'id' => 1,
                'name' => 'CFS',
                'created_at' => '2026-04-27 10:59:38',
                'updated_at' => '2026-04-27 10:59:38',
            ],
            [
                'id' => 2,
                'name' => 'ICT',
                'created_at' => '2026-04-27 10:59:38',
                'updated_at' => '2026-04-27 10:59:38',
            ],
            [
                'id' => 3,
                'name' => 'HSE',
                'created_at' => '2026-04-27 10:59:38',
                'updated_at' => '2026-04-27 10:59:38',
            ],
        ];

        $isSqlsrv = DB::connection()->getDriverName() === 'sqlsrv';

        if ($isSqlsrv) {
            DB::unprepared('SET IDENTITY_INSERT organizers ON;');
        }

        foreach (array_chunk($records, 100) as $chunk) {
            DB::table('organizers')->upsert(
                $chunk,
                ['id'],
                ['name', 'updated_at']
            );
        }

        if ($isSqlsrv) {
            DB::unprepared('SET IDENTITY_INSERT organizers OFF;');
        }
    }
}
