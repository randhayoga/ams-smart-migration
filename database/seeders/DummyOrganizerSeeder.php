<?php

namespace Database\Seeders;

use App\Models\Master\Organizer;
use Illuminate\Database\Seeder;

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
