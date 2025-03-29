"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import { ethers } from "ethers"

interface DepositInfo {
  message: string
  deposit_address: string
  amount: number
}

// HSKDeposit contract ABI
const HSKDepositABI = [
  {
    "inputs": [],
    "name": "deposit",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "user",
        "type": "address"
      }
    ],
    "name": "getBalance",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

// HSK network settings
const HSK_RPC_URL = process.env.NEXT_PUBLIC_HSK_RPC_URL || 'https://mainnet.hsk.xyz'

export default function DepositPage() {
  const [depositInfo, setDepositInfo] = useState<DepositInfo | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [account, setAccount] = useState<string | null>(null)
  const [userBalance, setUserBalance] = useState('0')

  useEffect(() => {
    checkConnection()
    fetchDepositInfo()
    
    // Account change event listener
    if (window.ethereum) {
      window.ethereum.on('accountsChanged', (accounts: string[]) => {
        setAccount(accounts[0])
        if (accounts[0]) {
          fetchUserBalance(accounts[0])
        }
      })
    }
    
    return () => {
      if (window.ethereum) {
        window.ethereum.removeListener('accountsChanged', () => {})
      }
    }
  }, [])

  const checkConnection = async () => {
    if (window.ethereum) {
      try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' }) as string[]
        setAccount(accounts[0])
        if (accounts[0]) {
          await fetchUserBalance(accounts[0])
        }
      } catch (error) {
        console.error('Connection error:', error)
        toast.error("Failed to connect wallet")
      }
    } else {
      toast.error("Please install HashKey wallet")
    }
  }

  const fetchUserBalance = async (userAddress: string) => {
    if (!depositInfo?.deposit_address) return

    try {
      const provider = new ethers.providers.JsonRpcProvider(HSK_RPC_URL)
      const contract = new ethers.Contract(depositInfo.deposit_address, HSKDepositABI, provider)
      
      const balance = await contract.getBalance(userAddress)
      setUserBalance(ethers.utils.formatEther(balance))
    } catch (error) {
      console.error('Balance fetch error:', error)
      toast.error("Failed to fetch balance")
    }
  }

  const fetchDepositInfo = async () => {
    try {
      const token = localStorage.getItem("authToken")
      if (!token) {
        throw new Error("No authentication token found")
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/users/deposit/info`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (!response.ok) {
        throw new Error("Failed to fetch deposit info")
      }
      const data = await response.json()
      setDepositInfo(data)
      
      // Fetch balance after getting deposit info
      if (account) {
        await fetchUserBalance(account)
      }
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to fetch deposit information")
    }
  }

  const handleDeposit = async () => {
    if (!depositInfo || !account) return

    setIsLoading(true)
    try {
      if (!window.ethereum) {
        throw new Error("HashKey wallet is not installed")
      }

      // Switch to HSK network (chain ID needs to be updated for HSK network)
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: '0xb1' }], // Update with actual HSK network chain ID
      })

      // Connect wallet
      const provider = new ethers.providers.Web3Provider(window.ethereum)
      const signer = provider.getSigner()
      const contract = new ethers.Contract(depositInfo.deposit_address, HSKDepositABI, signer)

      // Convert amount to wei
      const amountWei = ethers.utils.parseEther(depositInfo.amount.toString())

      // Call deposit function
      const tx = await contract.deposit({ value: amountWei })
      toast.info("Transaction submitted. Waiting for confirmation...")

      // Wait for transaction confirmation
      await tx.wait()

      // Update balance after successful deposit
      await fetchUserBalance(account)

      toast.success("Deposit successful!")
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to send transaction")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Deposit</h1>
      <Card>
        <CardHeader>
          <CardTitle>Deposit Information</CardTitle>
        </CardHeader>
        <CardContent>
          {depositInfo ? (
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-500">Connected Wallet</p>
                <p className="font-mono break-all">{account || "Not connected"}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Current Balance</p>
                <p>{userBalance} HSK</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Deposit Amount</p>
                <p>{depositInfo.amount} HSK</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Message</p>
                <p>{depositInfo.message}</p>
              </div>
              <Button
                onClick={handleDeposit}
                disabled={isLoading || !account}
                className="w-full"
              >
                {isLoading ? "Processing..." : "Deposit with HashKey"}
              </Button>
            </div>
          ) : (
            <p>Loading deposit information...</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
} 