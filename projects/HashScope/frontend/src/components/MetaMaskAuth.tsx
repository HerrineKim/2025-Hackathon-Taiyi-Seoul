'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { useSDK } from '@metamask/sdk-react';
import type Web3 from 'web3';

const API_BASE_URL = 'https://hashkey.sungwoonsong.com';

interface NonceResponse {
  wallet_address: string;
  nonce: string;
  message: string;
}

interface VerifyResponse {
  access_token: string;
  token_type: string;
  wallet_address: string;
  token_balance: number;
}

interface ValidationError {
  detail: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}

declare global {
  interface Window {
    web3: Web3;
    ethereum: {
      request: (args: { method: string; params?: unknown[] }) => Promise<unknown>;
      isConnected: () => boolean;
      on: (eventName: string, callback: (accounts: string[]) => void) => void;
      removeListener: (eventName: string, callback: (accounts: string[]) => void) => void;
    };
  }
}

export default function MetaMaskAuth() {
  const { sdk } = useSDK();
  const [account, setAccount] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [tokenBalance, setTokenBalance] = useState<number | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isMetaMaskConnected, setIsMetaMaskConnected] = useState(false);

  // Function to check MetaMask connection
  const checkMetaMaskConnection = async () => {
    try {
      if (typeof window.ethereum !== 'undefined') {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        if (Array.isArray(accounts) && accounts.length > 0) {
          setIsMetaMaskConnected(true);
          setAccount(accounts[0] as string);
        } else {
          setIsMetaMaskConnected(false);
          setAccount(null);
        }
      }
    } catch (err) {
      console.error('Error checking MetaMask connection:', err);
      setIsMetaMaskConnected(false);
      setAccount(null);
    }
  };

  // Function to handle account changes
  const handleAccountsChanged = (accounts: string[]) => {
    if (accounts.length === 0) {
      setIsMetaMaskConnected(false);
      setAccount(null);
      setIsLoggedIn(false);
      localStorage.removeItem('authToken');
      localStorage.removeItem('account');
      localStorage.removeItem('tokenBalance');
    } else {
      setIsMetaMaskConnected(true);
      setAccount(accounts[0]);
    }
  };

  // Check for existing session and MetaMask connection on mount
  useEffect(() => {
    const checkExistingSession = async () => {
      const storedAccount = localStorage.getItem('account');
      const storedToken = localStorage.getItem('authToken');
      const storedBalance = localStorage.getItem('tokenBalance');

      if (storedAccount && storedToken) {
        setAccount(storedAccount);
        if (storedBalance) {
          setTokenBalance(Number(storedBalance));
        }
        setIsLoggedIn(true);
      }

      // Check MetaMask connection
      await checkMetaMaskConnection();

      // Set up event listeners
      if (typeof window.ethereum !== 'undefined') {
        window.ethereum.on('accountsChanged', handleAccountsChanged);
        window.ethereum.on('chainChanged', () => window.location.reload());
      }

      // Cleanup function
      return () => {
        if (typeof window.ethereum !== 'undefined') {
          window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
          window.ethereum.removeListener('chainChanged', () => window.location.reload());
        }
      };
    };

    checkExistingSession();
  }, []);

  const enableMetaMask = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (typeof window.ethereum === 'undefined') {
        throw new Error('Please install MetaMask!');
      }

      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      if (Array.isArray(accounts) && accounts.length > 0) {
        const newAccount = accounts[0] as string;
        setAccount(newAccount);
        setIsMetaMaskConnected(true);
        localStorage.setItem('account', newAccount);
      }
    } catch (err) {
      console.error('Error enabling MetaMask:', err);
      setError(err instanceof Error ? err.message : 'Failed to enable MetaMask');
      setIsMetaMaskConnected(false);
    } finally {
      setLoading(false);
    }
  };

  const loginWithMetaMask = async () => {
    if (!isMetaMaskConnected || !account) {
      setError('Please connect your wallet first');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // 1. Get nonce from backend
      const nonceResponse = await fetch(`${API_BASE_URL}/auth/nonce`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wallet_address: account
        }),
      });

      if (!nonceResponse.ok) {
        const errorData: ValidationError = await nonceResponse.json();
        throw new Error(errorData.detail[0]?.msg || 'Failed to get nonce');
      }

      const nonceData: NonceResponse = await nonceResponse.json();

      // 2. Sign the message using MetaMask
      const signature = await window.ethereum.request({
        method: 'personal_sign',
        params: [nonceData.message, account]
      }) as string;

      // 3. Verify signature with backend
      const verifyResponse = await fetch(`${API_BASE_URL}/auth/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wallet_address: account,
          signature: signature
        }),
      });

      if (!verifyResponse.ok) {
        const errorData: ValidationError = await verifyResponse.json();
        throw new Error(errorData.detail[0]?.msg || 'Failed to verify signature');
      }

      const verifyData: VerifyResponse = await verifyResponse.json();
      
      // Store the token and update balance
      localStorage.setItem('authToken', verifyData.access_token);
      localStorage.setItem('tokenBalance', verifyData.token_balance.toString());
      setTokenBalance(verifyData.token_balance);
      setIsLoggedIn(true);
    } catch (err) {
      console.error('Login error:', err);
      setError(err instanceof Error ? err.message : 'Failed to login');
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await sdk?.disconnect();
      setAccount(null);
      setTokenBalance(null);
      setIsLoggedIn(false);
      setIsMetaMaskConnected(false);
      localStorage.removeItem('authToken');
      localStorage.removeItem('account');
      localStorage.removeItem('tokenBalance');
    } catch (err) {
      console.warn(`Failed to disconnect`, err);
      setError('Failed to disconnect');
    }
  };

  return (
    <div className="w-full">
      {error && (
        <div className="mb-6 p-4 bg-red-900/50 rounded-lg">
          <p className="text-red-200">{error}</p>
        </div>
      )}

      {isMetaMaskConnected && account && (
        <div className="mb-6 p-4 bg-green-900/50 rounded-lg">
          <h3 className="text-green-200 font-medium">Connected Account</h3>
          <p className="text-sm text-green-300 mt-1">{account}</p>
          {tokenBalance !== null && (
            <p className="text-sm text-green-300 mt-1">HSK Balance: {tokenBalance}</p>
          )}
          <div className="w-full bg-green-900/50 rounded-full h-2.5 mt-2">
            <div className="bg-green-500 h-2.5 rounded-full animate-pulse"></div>
          </div>
        </div>
      )}

      <section className="space-y-4">
        <button
          onClick={enableMetaMask}
          disabled={loading || isMetaMaskConnected}
          className="w-full flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Image src="/MetaMask_Fox.svg" alt="MetaMask Fox" className="w-6 h-6 mr-2" width={24} height={24} />
          {loading ? 'Connecting...' : isMetaMaskConnected ? 'Connected' : 'Connect Wallet'}
        </button>

        <button
          onClick={loginWithMetaMask}
          disabled={!isMetaMaskConnected || loading || isLoggedIn}
          className="w-full flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Image src="/MetaMask_Fox.svg" alt="MetaMask Fox" className="w-6 h-6 mr-2" width={24} height={24} />
          {loading ? 'Logging in...' : isLoggedIn ? 'Already Logged In' : 'Login with Wallet'}
        </button>

        {isMetaMaskConnected && (
          <button
            onClick={logout}
            disabled={loading}
            className="w-full flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Image src="/MetaMask_Fox.svg" alt="MetaMask Fox" className="w-6 h-6 mr-2" width={24} height={24} />
            Logout
          </button>
        )}
      </section>
    </div>
  );
} 