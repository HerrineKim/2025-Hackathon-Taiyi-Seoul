'use client';

import Link from 'next/link';
import { ArrowRight, Key, LineChart, Coins, Database } from 'lucide-react';
import { useSDK } from '@metamask/sdk-react';
import Image from 'next/image';
export default function Home() {
  const { connected } = useSDK();

  return (
    <div className="min-h-screen bg-gray-800">
      <main className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <Image
            src="/logo-500.png" 
            alt="HashScope Logo" 
            className="w-32 h-32 mx-auto mb-6"
            width={128}
            height={128}
          />
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">
            HashScope
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            An HSK Chain-based tokenized API platform providing real-time crypto data for Al agents.
          </p>
          <Link
            href={connected ? "/hot" : "/my/profile"}
            className="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg font-semibold rounded-lg transition-colors"
          >
            {connected ? 'Explore Hot APIs' : 'Get Started'} <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-gray-700 p-6 rounded-lg">
            <div className="flex items-center mb-4">
              <Key className="w-8 h-8 text-blue-500 mr-3" />
              <h3 className="text-xl font-semibold text-white">Secure API Access</h3>
            </div>
            <p className="text-gray-300">
              Stake HSK tokens to receive your secret key and start using our APIs
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg">
            <div className="flex items-center mb-4">
              <LineChart className="w-8 h-8 text-blue-500 mr-3" />
              <h3 className="text-xl font-semibold text-white">Real-time Data</h3>
            </div>
            <p className="text-gray-300">
              Access comprehensive crypto market data for AI predictions and automated trading
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg">
            <div className="flex items-center mb-4">
              <Coins className="w-8 h-8 text-blue-500 mr-3" />
              <h3 className="text-xl font-semibold text-white">Pay-as-you-go</h3>
            </div>
            <p className="text-gray-300">
              Pay only for what you use with our usage-based billing model
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg">
            <div className="flex items-center mb-4">
              <LineChart className="w-8 h-8 text-blue-500 mr-3" />
              <h3 className="text-xl font-semibold text-white">API Analytics</h3>
            </div>
            <p className="text-gray-300">
              Track your API usage, performance metrics, and cost analysis in real-time
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg">
            <div className="flex items-center mb-4">
              <Key className="w-8 h-8 text-blue-500 mr-3" />
              <h3 className="text-xl font-semibold text-white">API Management</h3>
            </div>
            <p className="text-gray-300">
              Create and manage API keys with customizable rate limits
            </p>
          </div>

          <div className="bg-gray-700 p-6 rounded-lg">
            <div className="flex items-center mb-4">
              <Database className="w-8 h-8 text-blue-500 mr-3" />
              <h3 className="text-xl font-semibold text-white">Rich API Collection</h3>
            </div>
            <p className="text-gray-300">
              Access diverse APIs for market data, social signals, and on-chain analytics
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
