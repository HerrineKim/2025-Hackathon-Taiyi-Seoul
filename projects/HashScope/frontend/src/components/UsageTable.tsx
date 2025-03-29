'use client';

import * as React from "react";
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export type UsageData = {
  id: string;
  apiName: string;
  totalUsage: number;
  totalCost: number;
  category: string;
};

const mockData: UsageData[] = [
  {
    id: "1",
    apiName: "HSK Latest Block",
    totalUsage: 1500,
    totalCost: 150,
    category: "On-chain data"
  },
  {
    id: "2",
    apiName: "HSK Exchange Inflow",
    totalUsage: 800,
    totalCost: 80,
    category: "On-chain data"
  },
  {
    id: "3",
    apiName: "BTC Price",
    totalUsage: 3000,
    totalCost: 300,
    category: "Exchange Data"
  },
  {
    id: "4",
    apiName: "HSK Price",
    totalUsage: 2500,
    totalCost: 250,
    category: "Exchange Data"
  },
  {
    id: "5",
    apiName: "Trump Social Media",
    totalUsage: 500,
    totalCost: 1000,
    category: "Social Media"
  },
  {
    id: "6",
    apiName: "Elon Musk Social Media",
    totalUsage: 400,
    totalCost: 800,
    category: "Social Media"
  }
];

export const columns: ColumnDef<UsageData>[] = [
  {
    accessorKey: "id",
    header: "Index",
    cell: ({ row }) => {
      return <div className="font-medium text-center">{Number(row.original.id)}</div>;
    },
  },
  {
    accessorKey: "apiName",
    header: "API Name",
    cell: ({ row }) => {
      return <div className="font-medium">{row.original.apiName}</div>;
    },
  },
  {
    accessorKey: "totalUsage",
    header: "Total Usage",
    cell: ({ row }) => {
      return <div className="text-right font-medium">{row.original.totalUsage.toLocaleString()}</div>;
    },
  },
  {
    accessorKey: "totalCost",
    header: "Total Cost (HSK)",
    cell: ({ row }) => {
      return <div className="text-right font-medium">{row.original.totalCost.toLocaleString()}</div>;
    },
  },
];

export function UsageTable() {
  const table = useReactTable({
    data: mockData,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="rounded-md border border-gray-700">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id} className="bg-gray-700">
              {headerGroup.headers.map((header) => {
                return (
                  <TableHead key={header.id} className="text-white">
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                );
              })}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
                className="bg-gray-800 text-white hover:bg-gray-700"
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id} className="py-4">
                    {flexRender(
                      cell.column.columnDef.cell,
                      cell.getContext()
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell
                colSpan={columns.length}
                className="h-24 text-center text-white"
              >
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
} 