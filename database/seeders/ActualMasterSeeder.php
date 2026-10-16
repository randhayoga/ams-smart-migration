<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class ActualMasterSeeder extends Seeder
{
    /**
     * Run the actual/final master data seeds in relational dependency order.
     */
    public function run(): void
    {
        $this->call([
            ActualCategorySeeder::class,
            ActualTypeSeeder::class,
            ActualUomSeeder::class,
            ActualBrandSeeder::class,
            ActualVendorSeeder::class,
            ActualOrganizerSeeder::class,
            ActualLocationSeeder::class,
        ]);
    }
}
