"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"

interface DepositInfo {
  message: string
  deposit_address: string
  amount: number
}

interface HashKeyProvider {
  request: (args: { method: string; params?: unknown[] }) => Promise<unknown>
  isConnected: () => boolean
  on: (eventName: string, callback: (accounts: string[]) => void) => void
  removeListener: (eventName: string, callback: (accounts: string[]) => void) => void
  utils: {
    toWei: (value: string, unit: string) => string
  }
}

declare global {
  interface Window {
    hashkey?: HashKeyProvider
  }
}

export default function DepositPage() {
  const [depositInfo, setDepositInfo] = useState<DepositInfo | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    fetchDepositInfo()
  }, [])

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
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to fetch deposit information")
    }
  }

  const handleDeposit = async () => {
    if (!depositInfo) return

    setIsLoading(true)
    try {
      const hashkey = window.hashkey as HashKeyProvider | undefined
      if (!hashkey) {
        throw new Error("HashKey is not installed")
      }

      const accounts = await hashkey.request({
        method: "eth_requestAccounts",
      }) as string[]

      const transaction = {
        from: accounts[0],
        to: depositInfo.deposit_address,
        value: hashkey.utils.toWei(depositInfo.amount.toString(), "ether"),
      }

      const txHash = await hashkey.request({
        method: "eth_sendTransaction",
        params: [transaction],
      })

      toast.success(`Transaction sent! Hash: ${txHash}`)
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
                <p className="text-sm text-gray-500">Deposit Address</p>
                <p className="font-mono break-all">{depositInfo.deposit_address}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Amount</p>
                <p>{depositInfo.amount} HSK</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Message</p>
                <p>{depositInfo.message}</p>
              </div>
              <Button
                onClick={handleDeposit}
                disabled={isLoading}
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