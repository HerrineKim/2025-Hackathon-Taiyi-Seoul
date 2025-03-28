'use client';

import Link from 'next/link';
import Header from './components/Header';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-800">
      <Header />
      <main className="px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full py-8">
        <div className="w-full max-w-md mb-16">
          <div className="space-y-4">
            <Link
              href="/sign-in"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-6 text-lg font-semibold"
            >
              Sign in
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
