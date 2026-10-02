<?php

namespace Database\Seeders;

use App\Models\Master\Uom;
use Illuminate\Database\Seeder;

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
