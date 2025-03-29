'use client';

import { UsageTable } from '@/components/UsageTable';
import { Coins } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function UsagePage() {
  const [tokenBalance, setTokenBalance] = useState<number | null>(null);

  useEffect(() => {
    const storedBalance = localStorage.getItem('tokenBalance');
    if (storedBalance) {
      setTokenBalance(Number(storedBalance));
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-800 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-white">API Usage</h1>
          <div className="flex items-center space-x-2 bg-gray-700 px-4 py-2 rounded-lg">
            <Coins className="w-5 h-5 text-yellow-400" />
            <span className="text-white font-semibold">
              {tokenBalance !== null ? `${tokenBalance.toLocaleString()} HSK` : 'Not Connected'}
            </span>
          </div>
        </div>

        <div className="bg-gray-700 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-6">Usage Statistics</h2>
          <UsageTable />
        </div>
      </div>
    </div>
  );
} 