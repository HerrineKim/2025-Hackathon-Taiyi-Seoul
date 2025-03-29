'use client';

import { UsageTable } from '@/components/UsageTable';

export default function UsagePage() {
  return (
    <div className="min-h-screen bg-gray-800 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">API Usage</h1>

        <div className="bg-gray-700 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-6">Usage Statistics</h2>
          <UsageTable />
        </div>
      </div>
    </div>
  );
} 