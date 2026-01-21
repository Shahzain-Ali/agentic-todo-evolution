import LoginForm from '@/components/LoginForm';
import Link from 'next/link';

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ registered?: string }>;
}) {
  const params = await searchParams;

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-500 via-blue-600 to-indigo-700 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <div className="w-16 h-16 bg-white/10 backdrop-blur-lg rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl">
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </Link>
          <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-blue-100">Sign in to continue to your tasks</p>
        </div>

        {/* Success Message */}
        {params.registered === 'true' && (
          <div className="mb-6 bg-green-500/20 backdrop-blur-lg border-2 border-green-400/50 text-white px-6 py-4 rounded-2xl shadow-xl animate-in fade-in slide-in-from-top-3">
            <div className="flex items-center gap-3">
              <svg className="w-6 h-6 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p className="font-semibold">Account created successfully!</p>
                <p className="text-sm text-blue-100">Please sign in to continue</p>
              </div>
            </div>
          </div>
        )}

        {/* Form Card */}
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/20">
          <LoginForm />
        </div>

        {/* Create Account Link */}
        <p className="mt-6 text-center text-sm text-blue-100">
          Don't have an account?{' '}
          <Link href="/register" className="font-semibold text-white hover:underline transition-all">
            Create one
          </Link>
        </p>
      </div>
    </main>
  );
}
