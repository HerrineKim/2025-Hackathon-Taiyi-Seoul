'use client';

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

type EndpointHistory = {
  endpoint: string;
  method: string;
  call_count: number;
  last_used_at: string;
  total_cost: number;
};

type ApiKeyHistory = {
  key_id: string;
  total_calls: number;
  total_cost: number;
  endpoints: EndpointHistory[];
};

export default function ApiKeyHistoryPage() {
  const params = useParams();
  const [data, setData] = useState<ApiKeyHistory | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api-keys/${params.key_id}/history`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch API key history');
        }

        const history = await response.json();
        setData(history);
      } catch (error) {
        console.error('Error fetching API key history:', error);
        setError('Failed to fetch API key history. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, [params.key_id]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-white">Loading API key history...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">{error}</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-white">No history found.</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="text-gray-400 text-sm">Total Calls</h3>
          <p className="text-2xl font-bold text-white">{data.total_calls.toLocaleString()}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="text-gray-400 text-sm">Total Cost</h3>
          <p className="text-2xl font-bold text-white">{data.total_cost.toLocaleString()} HSK</p>
        </div>
      </div>

      <div className="rounded-md border border-gray-700">
        <Table>
          <TableHeader>
            <TableRow className="bg-gray-700">
              <TableHead className="text-white">Endpoint</TableHead>
              <TableHead className="text-white">Method</TableHead>
              <TableHead className="text-white text-right">Calls</TableHead>
              <TableHead className="text-white">Last Used</TableHead>
              <TableHead className="text-white text-right">Cost (HSK)</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.endpoints.map((endpoint, index) => (
              <TableRow key={index} className="bg-gray-800 text-white hover:bg-gray-700">
                <TableCell className="font-medium">{endpoint.endpoint}</TableCell>
                <TableCell className="font-medium">{endpoint.method}</TableCell>
                <TableCell className="text-right font-medium">{endpoint.call_count.toLocaleString()}</TableCell>
                <TableCell className="font-medium">
                  {new Date(endpoint.last_used_at).toLocaleString()}
                </TableCell>
                <TableCell className="text-right font-medium">{endpoint.total_cost.toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
} 