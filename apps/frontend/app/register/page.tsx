import RegisterForm from '@/components/RegisterForm';
import Link from 'next/link';

export default function RegisterPage() {
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
          <h1 className="text-3xl font-bold text-text-primary mb-2">Create Account</h1>
          <p className="text-text-secondary">Start organizing your tasks today</p>
        </div>

        {/* Form Card */}
        <div className="bg-background rounded-2xl shadow-xl p-8 border border-border">
          <RegisterForm />
        </div>

        {/* Sign In Link */}
        <p className="mt-6 text-center text-sm text-text-secondary">
          Already have an account?{' '}
          <Link href="/login" className="font-semibold text-primary hover:text-primary-dark hover:underline transition-all">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
