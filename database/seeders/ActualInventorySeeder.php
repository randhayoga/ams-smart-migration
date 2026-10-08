<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class ActualInventorySeeder extends Seeder
{
    /**
     * Run the actual Inventory database seeds in relational dependency order.
     * Order:
     * 1. Barangs (665 items)
     * 2. Lots (665 items)
     * 3. Units (6,939 items)
     */
    public function run(): void
    {
        $this->call([
            ActualBarangSeeder::class,
            ActualLotSeeder::class,
            ActualUnitSeeder::class,
        ]);
    }
}
