'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Coins, ArrowRight } from 'lucide-react';

interface TierInfo {
  name: string;
  color: string;
  feeRate: number;
  rateLimit: number;
  minBalance: number;
  description: string;
}

const tiers: TierInfo[] = [
  {
    name: 'Gold',
    color: 'from-yellow-400 to-yellow-600',
    feeRate: 0.5,
    rateLimit: 1000,
    minBalance: 10000,
    description: 'Best for high-volume traders and professional users'
  },
  {
    name: 'Silver',
    color: 'from-gray-400 to-gray-600',
    feeRate: 1.0,
    rateLimit: 500,
    minBalance: 5000,
    description: 'Perfect for active traders and regular users'
  },
  {
    name: 'Bronze',
    color: 'from-amber-700 to-amber-900',
    feeRate: 2.0,
    rateLimit: 100,
    minBalance: 1000,
    description: 'Great for getting started with basic features'
  }
];

export default function TierPage() {
  const [tokenBalance, setTokenBalance] = useState<number | null>(null);
  const [currentTier, setCurrentTier] = useState<string>('Bronze');

  useEffect(() => {
    const storedBalance = localStorage.getItem('tokenBalance');
    if (storedBalance) {
      const balance = Number(storedBalance);
      setTokenBalance(balance);
      
      // Determine current tier based on balance
      if (balance >= 10000) {
        setCurrentTier('Gold');
      } else if (balance >= 5000) {
        setCurrentTier('Silver');
      } else if (balance >= 1000) {
        setCurrentTier('Bronze');
      }
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-800 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8 text-center">Subscription Tiers</h1>
        
        {/* Tier Boxes */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          {tiers.map((tier) => (
            <div
              key={tier.name}
              className={`relative bg-gradient-to-b ${tier.color} rounded-lg p-6 shadow-lg transform transition-transform hover:scale-105 ${
                currentTier === tier.name ? 'ring-4 ring-white' : ''
              }`}
            >
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div className="bg-white text-gray-900 px-4 py-1 rounded-full text-sm font-semibold">
                  {tier.name}
                </div>
              </div>
              <div className="mt-4 text-white">
                <h3 className="text-xl font-bold mb-4">{tier.name} Tier</h3>
                <div className="space-y-3">
                  <p className="flex justify-between">
                    <span>Fee Rate:</span>
                    <span className="font-semibold">{tier.feeRate}%</span>
                  </p>
                  <p className="flex justify-between">
                    <span>Rate Limit:</span>
                    <span className="font-semibold">{tier.rateLimit}/min</span>
                  </p>
                  <p className="flex justify-between">
                    <span>Min Balance:</span>
                    <span className="font-semibold">{tier.minBalance} HSK</span>
                  </p>
                </div>
                <p className="mt-4 text-sm opacity-90">{tier.description}</p>
              </div>
            </div>
          ))}
        </div>

        {/* User Balance Section */}
        <div className="bg-gray-700 rounded-lg p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-white mb-2">Your Current Balance</h2>
              <div className="flex items-center space-x-2">
                <Coins className="w-6 h-6 text-yellow-400" />
                <span className="text-2xl font-bold text-white">
                  {tokenBalance !== null ? `${tokenBalance.toLocaleString()} HSK` : 'Not Connected'}
                </span>
              </div>
            </div>
            <div className="text-right">
              <p className="text-gray-300">Current Tier</p>
              <span className="text-xl font-bold text-white">{currentTier}</span>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="text-center">
          <Link
            href="/my/profile"
            className="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg font-semibold rounded-lg transition-colors"
          >
            Deposit and upgrade your tier now
            <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
        </div>
      </div>
    </div>
  );
} 