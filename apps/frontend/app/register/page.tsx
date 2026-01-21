import RegisterForm from '@/components/RegisterForm';
import Link from 'next/link';

export default function RegisterPage() {
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
          <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
          <p className="text-blue-100">Start organizing your tasks today</p>
        </div>

        {/* Form Card */}
        <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/20">
          <RegisterForm />
        </div>

        {/* Sign In Link */}
        <p className="mt-6 text-center text-sm text-blue-100">
          Already have an account?{' '}
          <Link href="/login" className="font-semibold text-white hover:underline transition-all">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
