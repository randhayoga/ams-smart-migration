<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class ActualInventorySeeder extends Seeder
{
    /**
     * Run the actual Inventory database seeds in relational dependency order.
     * Order:
     * 1. Models (650 items)
     * 2. Lots (659 items)
     * 3. Assets (6,515 items)
     */
    public function run(): void
    {
        $this->call([
            ActualModelSeeder::class,
            ActualLotSeeder::class,
            ActualAssetSeeder::class,
        ]);
    }
}
