<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class ActualDatabaseSeeder extends Seeder
{
    /**
     * Run the complete production actual database seeds.
     * Order:
     * 1. Master Data (Categories, Subcategories, UOMs, Brands, Vendors, Organizers, Locations)
     * 2. Inventory Data (Barangs, Lots, Units)
     */
    public function run(): void
    {
        $this->call([
            ActualMasterSeeder::class,
            ActualInventorySeeder::class,
        ]);
    }
}
