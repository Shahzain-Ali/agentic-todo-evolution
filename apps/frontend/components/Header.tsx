'use client';

import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';
import {
  Menu,
  Bell,
  Calendar as CalendarIcon,
  LayoutGrid,
  LogOut,
} from 'lucide-react';

interface HeaderProps {
  onMenuClick?: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
  const router = useRouter();

  const handleLogout = async () => {
    // Use Better Auth sign out
    await authClient.signOut();
    router.push('/login');
  };

  return (
    <header className="bg-background border-b border-border sticky top-0 z-30">
      <div className="flex justify-between items-center h-14 px-4 lg:px-6">
        {/* Left: Hamburger Menu (Mobile Only) */}
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 hover:bg-background-subtle rounded-lg transition-colors"
            aria-label="Open menu"
          >
            <Menu className="w-5 h-5 text-text-secondary" />
          </button>
        </div>

        {/* Right: Utility Buttons */}
        <div className="flex items-center gap-2">
          {/* Notifications */}
          <button
            className="p-2 hover:bg-background-subtle rounded-lg transition-colors"
            aria-label="Notifications"
          >
            <Bell className="w-5 h-5 text-text-secondary" />
          </button>

          {/* Calendar Connect */}
          <button className="hidden sm:flex items-center gap-2 px-3 py-1.5 text-sm text-text-secondary hover:text-text-primary hover:bg-background-subtle rounded-lg transition-colors">
            <CalendarIcon className="w-4 h-4" />
            <span className="hidden md:inline">Connect calendar</span>
          </button>

          {/* Display Options */}
          <button
            className="p-2 hover:bg-background-subtle rounded-lg transition-colors"
            aria-label="Display options"
          >
            <LayoutGrid className="w-5 h-5 text-text-secondary" />
          </button>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="p-2 hover:bg-background-subtle rounded-lg transition-colors text-text-secondary hover:text-danger"
            aria-label="Logout"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}
