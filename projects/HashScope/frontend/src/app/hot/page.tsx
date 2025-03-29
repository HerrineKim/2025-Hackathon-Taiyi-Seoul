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
import { ArrowUpRight, TrendingUp, Users, LineChart, Flame } from 'lucide-react';
import { Pagination } from "@/components/ui/pagination";

interface HotAPI {
  id: string;
  name: string;
  description: string;
  category: string;
  usage: number;
  price: number;
  icon: React.ReactNode;
  trend: number; // Percentage increase in usage
}

const hotAPIs: HotAPI[] = [
  {
    id: "1",
    name: "BTC Price Feed",
    description: "Real-time Bitcoin price data from major exchanges",
    category: "Market Data",
    usage: 15000,
    price: 0.1,
    icon: <TrendingUp className="w-5 h-5" />,
    trend: 45
  },
  {
    id: "2",
    name: "HSK Price Feed",
    description: "Live HSK token price and market data",
    category: "Market Data",
    usage: 12000,
    price: 0.1,
    icon: <TrendingUp className="w-5 h-5" />,
    trend: 32
  },
  {
    id: "3",
    name: "Trump Social Sentiment",
    description: "Real-time sentiment analysis of Trump's social media posts",
    category: "Social Signals",
    usage: 8000,
    price: 0.5,
    icon: <Users className="w-5 h-5" />,
    trend: 78
  },
  {
    id: "4",
    name: "Elon Musk Impact",
    description: "Market impact analysis of Elon Musk's tweets",
    category: "Social Signals",
    usage: 7500,
    price: 0.5,
    icon: <Users className="w-5 h-5" />,
    trend: 65
  },
  {
    id: "5",
    name: "HSK Network Activity",
    description: "Real-time network activity and transaction volume",
    category: "On-chain Analytics",
    usage: 10000,
    price: 0.2,
    icon: <LineChart className="w-5 h-5" />,
    trend: 28
  },
  {
    id: "6",
    name: "Exchange Flow Analysis",
    description: "HSK token flow analysis between exchanges",
    category: "On-chain Analytics",
    usage: 9000,
    price: 0.2,
    icon: <LineChart className="w-5 h-5" />,
    trend: 42
  }
];

const trendingSearches = [
  "BTC Price Feed",
  "Trump Social Sentiment",
  "HSK Network Activity",
  "Elon Musk Impact",
  "Exchange Flow Analysis",
  "HSK Price Feed"
];

const ITEMS_PER_PAGE = 6;

export default function HotPage() {
  const [selectedCategory, setSelectedCategory] = React.useState<string>("all");
  const [currentSuggestion, setCurrentSuggestion] = React.useState(0);
  const [currentPage, setCurrentPage] = React.useState(1);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSuggestion((prev) => (prev + 1) % trendingSearches.length);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const filteredAPIs = selectedCategory === "all" 
    ? hotAPIs 
    : hotAPIs.filter(api => api.category === selectedCategory);

  const totalPages = Math.ceil(filteredAPIs.length / ITEMS_PER_PAGE);
  const paginatedAPIs = filteredAPIs.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  // Reset to first page when category changes
  React.useEffect(() => {
    setCurrentPage(1);
  }, [selectedCategory]);

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
                  {trendingSearches[currentSuggestion]}
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
                <SelectItem value="Market Data" className="text-white hover:bg-gray-600">Market Data</SelectItem>
                <SelectItem value="Social Signals" className="text-white hover:bg-gray-600">Social Signals</SelectItem>
                <SelectItem value="On-chain Analytics" className="text-white hover:bg-gray-600">On-chain Analytics</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {paginatedAPIs.map((api) => (
            <div
              key={api.id}
              className="bg-gray-700 rounded-lg p-6 hover:bg-gray-600 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
                    {api.icon}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">{api.name}</h3>
                    <p className="text-sm text-gray-400">{api.category}</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-2 text-green-400">
                    <Flame className="w-4 h-4" />
                    <span className="text-sm">+{api.trend}%</span>
                  </div>
                  <div className="text-sm text-gray-400 mt-1">Usage</div>
                  <div className="text-white font-medium">{api.usage.toLocaleString()}</div>
                </div>
              </div>
              <p className="mt-4 text-gray-300">{api.description}</p>
              <div className="mt-4 flex items-center justify-between">
                <div className="text-sm text-gray-400">
                  Price: <span className="text-white">{api.price} HSK</span> / call
                </div>
                <button className="text-blue-400 hover:text-blue-300 text-sm font-medium flex items-center">
                  Try it now <ArrowUpRight className="w-4 h-4 ml-1" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Pagination */}
        {filteredAPIs.length > 0 && (
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