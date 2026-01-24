'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    if (token) {
      // Redirect authenticated users to dashboard
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-700">
      <div className="min-h-screen flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8">
        <div className="max-w-5xl w-full">
          {/* Hero Section */}
          <div className="text-center mb-12 space-y-6">
            <div className="inline-block">
              <div className="flex items-center justify-center w-20 h-20 bg-white/10 backdrop-blur-lg rounded-3xl mb-6 mx-auto shadow-xl">
                <svg className="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>

            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white tracking-tight">
              Get things done
            </h1>
            <p className="text-xl sm:text-2xl text-blue-100 max-w-2xl mx-auto font-light">
              The simple, powerful way to manage your tasks and stay organized
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
              <Link
                href="/register"
                className="group w-full sm:w-auto px-10 py-4 bg-white text-blue-600 rounded-2xl font-semibold text-lg shadow-2xl hover:shadow-white/20 hover:scale-105 transition-all duration-300 ease-out"
              >
                <span className="flex items-center justify-center gap-2">
                  Get Started Free
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
              </Link>
              <Link
                href="/login"
                className="w-full sm:w-auto px-10 py-4 bg-white/10 backdrop-blur-lg text-white rounded-2xl font-semibold text-lg border-2 border-white/20 hover:bg-white/20 hover:border-white/30 transition-all duration-300"
              >
                Sign In
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20">
            <div className="group bg-white/10 backdrop-blur-lg p-8 rounded-3xl border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105 hover:shadow-2xl">
              <div className="w-14 h-14 bg-blue-500 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Simple & Intuitive</h3>
              <p className="text-blue-100 leading-relaxed">
                Clean interface designed for focus. Add tasks in seconds and get back to what matters.
              </p>
            </div>

            <div className="group bg-white/10 backdrop-blur-lg p-8 rounded-3xl border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105 hover:shadow-2xl">
              <div className="w-14 h-14 bg-indigo-500 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Lightning Fast</h3>
              <p className="text-blue-100 leading-relaxed">
                Real-time sync and instant updates. Your tasks are always up to date across all devices.
              </p>
            </div>

            <div className="group bg-white/10 backdrop-blur-lg p-8 rounded-3xl border border-white/20 hover:bg-white/15 transition-all duration-300 hover:scale-105 hover:shadow-2xl">
              <div className="w-14 h-14 bg-purple-500 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Secure & Private</h3>
              <p className="text-blue-100 leading-relaxed">
                Your data is encrypted and secure. We never share your information with anyone.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
