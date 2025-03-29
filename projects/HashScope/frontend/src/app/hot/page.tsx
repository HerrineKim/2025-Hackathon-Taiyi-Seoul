'use client';

import * as React from "react";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Flame, LineChart, Users, Database, Coins } from 'lucide-react';
import { Pagination } from "@/components/ui/pagination";
import apiService, { APICatalogItem, APICategoriesResponse } from "@/lib/api-service";

const ITEMS_PER_PAGE = 6;

// Helper function to get icon based on category
const getCategoryIcon = (category: string) => {
  switch (category.toLowerCase()) {
    case 'market data':
      return <LineChart className="w-5 h-5" />;
    case 'social signals':
      return <Users className="w-5 h-5" />;
    case 'on-chain analytics':
      return <Database className="w-5 h-5" />;
    default:
      return <Coins className="w-5 h-5" />;
  }
};

export default function HotPage() {
  const [selectedCategory, setSelectedCategory] = React.useState<string>("all");
  const [currentSuggestion, setCurrentSuggestion] = React.useState(0);
  const [currentPage, setCurrentPage] = React.useState(1);
  const [apis, setApis] = React.useState<APICatalogItem[]>([]);
  const [categories, setCategories] = React.useState<APICategoriesResponse>({});
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const [catalogResponse, categoriesResponse] = await Promise.all([
          apiService.listAPICatalog(selectedCategory === "all" ? undefined : selectedCategory),
          apiService.listAPICategories()
        ]);
        setApis(catalogResponse.apis);
        setCategories(categoriesResponse);
      } catch (error) {
        console.error('Error fetching API data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedCategory]);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSuggestion((prev) => (prev + 1) % apis.length);
    }, 2000);
    return () => clearInterval(interval);
  }, [apis.length]);

  const totalPages = Math.ceil(apis.length / ITEMS_PER_PAGE);
  const paginatedAPIs = apis.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  // Reset to first page when category changes
  React.useEffect(() => {
    setCurrentPage(1);
  }, [selectedCategory]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-800 p-6 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-800 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Dynamic Trending Section */}
        <div className="relative mb-12">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-lg blur-xl"></div>
          <div className="relative bg-gray-700/50 rounded-lg p-8 backdrop-blur-sm">
            <div className="flex items-center justify-center space-x-2">
              <Flame className="w-5 h-5 text-orange-400" />
              <div className="text-xl text-white font-medium">
                Trending now:{" "}
                <span className="text-orange-400 animate-fade-in-out">
                  {apis[currentSuggestion]?.summary || "Loading..."}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Trending APIs</h1>
            <p className="text-gray-400 mt-2">Most popular and fastest growing APIs this week</p>
          </div>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger className="w-[200px] bg-gray-700 text-white border-gray-600">
              <SelectValue placeholder="Select category" />
            </SelectTrigger>
            <SelectContent className="bg-gray-700 border-gray-600">
              <SelectGroup>
                <SelectLabel className="text-gray-400">Categories</SelectLabel>
                <SelectItem value="all" className="text-white hover:bg-gray-600">All Categories</SelectItem>
                {Object.entries(categories).map(([key, value]) => (
                  <SelectItem key={key} value={key} className="text-white hover:bg-gray-600">
                    {value}
                  </SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {paginatedAPIs.map((api) => (
            <div
              key={api.path}
              className="bg-gray-700 rounded-lg p-6 hover:bg-gray-600 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
                    {getCategoryIcon(api.category)}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">{api.summary}</h3>
                    <p className="text-sm text-gray-400">{api.category}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-2 text-green-400">
                    <Flame className="w-4 h-4" />
                    <span className="text-sm">+{Math.floor(Math.random() * 30) + 10}%</span>
                  </div>
                  <div className="text-sm text-gray-400 mt-1">Method</div>
                  <div className="text-white font-medium">{api.method}</div>
                </div>
              </div>
              <p className="mt-4 text-gray-300">{api.description}</p>
              <div className="mt-4">
                <div className="text-sm text-gray-400">
                  Path: <span className="text-white">{api.path}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Pagination */}
        {apis.length > 0 && (
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        )}
      </div>
    </div>
  );
} 