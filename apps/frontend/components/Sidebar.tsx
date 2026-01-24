'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Calendar,
  Clock,
  CheckCircle,
  Plus,
  Search,
  User,
  HelpCircle,
  X,
} from 'lucide-react';

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
  onAddTask?: () => void;
}

export default function Sidebar({ isOpen = true, onClose, onAddTask }: SidebarProps) {
  const pathname = usePathname();
  const [searchQuery, setSearchQuery] = useState('');

  const navItems = [
    {
      name: 'Today',
      href: '/dashboard',
      icon: Calendar,
      active: pathname === '/dashboard',
    },
    {
      name: 'Upcoming',
      href: '/dashboard/upcoming',
      icon: Clock,
      active: pathname === '/dashboard/upcoming',
    },
    {
      name: 'Completed',
      href: '/dashboard/completed',
      icon: CheckCircle,
      active: pathname === '/dashboard/completed',
    },
  ];

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:sticky top-0 left-0 z-50 h-screen
          w-sidebar bg-background border-r border-border
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          flex flex-col
        `}
      >
        {/* Header Section */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center justify-between mb-4">
            {/* User Profile */}
            <button className="flex items-center gap-2 hover:bg-background-subtle rounded-lg p-2 transition-colors">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-semibold text-text-primary">
                User
              </span>
            </button>

            {/* Close button (mobile only) */}
            <button
              onClick={onClose}
              className="lg:hidden p-2 hover:bg-background-subtle rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-text-secondary" />
            </button>
          </div>

          {/* Add Task Button */}
          <button
            onClick={onAddTask}
            className="w-full flex items-center gap-3 px-4 py-2.5 bg-primary hover:bg-primary-dark text-white rounded-lg transition-colors font-medium text-sm"
          >
            <Plus className="w-5 h-5" />
            Add task
          </button>
        </div>

        {/* Search Section */}
        <div className="p-4 border-b border-border">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-tertiary" />
            <input
              type="text"
              placeholder="Search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-background-subtle border border-border rounded-lg text-sm text-text-primary placeholder:text-text-tertiary focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
            />
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="flex-1 p-4 overflow-y-auto">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    onClick={onClose}
                    className={`
                      flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all
                      ${
                        item.active
                          ? 'bg-primary/10 text-primary'
                          : 'text-text-secondary hover:bg-background-subtle hover:text-text-primary'
                      }
                    `}
                  >
                    <Icon className="w-5 h-5" />
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Footer Section */}
        <div className="p-4 border-t border-border">
          <button className="flex items-center gap-2 px-3 py-2 text-sm text-text-secondary hover:text-text-primary hover:bg-background-subtle rounded-lg transition-colors w-full">
            <HelpCircle className="w-5 h-5" />
            Help & resources
          </button>
        </div>
      </aside>
    </>
  );
}
