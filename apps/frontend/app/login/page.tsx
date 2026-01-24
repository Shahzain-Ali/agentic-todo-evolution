import LoginForm from '@/components/LoginForm';
import Link from 'next/link';

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ registered?: string }>;
}) {
  const params = await searchParams;

  return (
    <main className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <div className="w-16 h-16 bg-primary rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </Link>
          <h1 className="text-3xl font-bold text-text-primary mb-2">Welcome Back</h1>
          <p className="text-text-secondary">Sign in to continue to your tasks</p>
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
                <p className="text-sm text-text-secondary">Please sign in to continue</p>
              </div>
            </div>
          </div>
        )}

        {/* Form Card */}
        <div className="bg-background rounded-2xl shadow-xl p-8 border border-border">
          <LoginForm />
        </div>

        {/* Create Account Link */}
        <p className="mt-6 text-center text-sm text-text-secondary">
          Don't have an account?{' '}
          <Link href="/register" className="font-semibold text-primary hover:text-primary-dark hover:underline transition-all">
            Create one
          </Link>
        </p>
      </div>
    </main>
  );
}
