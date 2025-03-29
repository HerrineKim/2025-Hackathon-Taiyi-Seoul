'use client';

import { SidebarTrigger } from "@/components/ui/sidebar"
import Image from 'next/image';
import { useSDK } from '@metamask/sdk-react';
import { formatAddress } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import Link from "next/link";
import { Coins } from 'lucide-react';
import { useEffect, useState } from 'react';

export function TopBar() {
  const { connected, account } = useSDK();
  const [tokenBalance, setTokenBalance] = useState<number | null>(null);

  useEffect(() => {
    const storedBalance = localStorage.getItem('tokenBalance');
    if (storedBalance) {
      setTokenBalance(Number(storedBalance));
    }
  }, []);

  return (
    <div className="sticky top-0 z-20 bg-gray-800 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-full items-center justify-between p-4 bg-gray-800">
        <div className="flex items-center">
          <SidebarTrigger className="bg-gray-800 text-white mr-4" />
          <Link href="/" className="flex items-center hover:opacity-90 transition-opacity">
            <Image src="/logo-500.png" alt="Logo" className="w-8 h-8 mr-2" width={20} height={20} />
            <span className="text-gray-100 text-lg sm:text-xl font-semibold">HashScope</span>
          </Link>
        </div>
        <div className="flex items-center space-x-4">
          {connected && (
            <div className="flex items-center space-x-2 bg-gray-700 px-3 py-1.5 rounded-lg">
              <Coins className="w-4 h-4 text-yellow-400" />
              <span className="text-white font-medium">
                {tokenBalance !== null ? `${tokenBalance.toLocaleString()} HSK` : '0 HSK'}
              </span>
            </div>
          )}
          <Link href="/my/profile">
            <Button 
              className="flex items-center justify-center bg-blue-600 text-white px-3 py-1.5 sm:px-4 sm:py-2 text-sm sm:text-base rounded-md hover:bg-blue-700 transition-colors"
            >
              {connected ? (
                <>
                  {formatAddress(account)} <Image src="/MetaMask_Fox.svg" alt="MetaMask Fox" className="inline-block w-4 h-4 ml-2" width={20} height={20} />
                </>
              ) : (
                'Sign In'
              )}
            </Button>
          </Link>
        </div>
      </div>
    </div>
  )
} 