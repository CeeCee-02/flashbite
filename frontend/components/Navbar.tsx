"use client";

import Link from "next/link";
import { useAuthStore } from "../store/authStore";
import { useEffect } from "react";
import { ShoppingBag, User, LogOut, Utensils, Bike, ShieldCheck } from "lucide-react";

export default function Navbar() {
  const { user, isAuthenticated, logout, initAuth } = useAuthStore();

  useEffect(() => {
    initAuth();
  }, [initAuth]);

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-orange-600 flex items-center justify-center text-white font-black text-xl shadow-md shadow-orange-200">
            ⚡
          </div>
          <span className="font-extrabold text-2xl tracking-tight text-slate-900">
            FLASH<span className="text-orange-600">BITE</span>
          </span>
        </Link>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-semibold text-slate-600">
          <Link href="/customer/login" className="hover:text-orange-600 transition">
            Order Food
          </Link>
          <Link href="/restaurant/login" className="hover:text-orange-600 transition flex items-center gap-1">
            <Utensils className="w-4 h-4 text-orange-600" />
            Partner Restaurant
          </Link>
          <Link href="/rider/login" className="hover:text-orange-600 transition flex items-center gap-1">
            <Bike className="w-4 h-4 text-orange-600" />
            Deliver as Rider
          </Link>
        </nav>

        {/* User Action Buttons */}
        <div className="flex items-center gap-3">
          {isAuthenticated && user ? (
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium text-slate-700 bg-slate-100 px-3 py-1.5 rounded-full flex items-center gap-2">
                <User className="w-4 h-4 text-orange-600" />
                {user.full_name} ({user.role})
              </span>
              <button
                onClick={() => logout()}
                className="text-sm font-medium text-rose-600 hover:text-rose-700 flex items-center gap-1 bg-rose-50 px-3 py-1.5 rounded-lg border border-rose-100 transition"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                href="/customer/login"
                className="text-sm font-medium text-slate-700 hover:text-slate-900 px-3 py-2 rounded-lg transition"
              >
                Sign In
              </Link>
              <Link
                href="/customer/register"
                className="text-sm font-semibold text-white bg-orange-600 hover:bg-orange-700 px-4 py-2 rounded-lg shadow-sm shadow-orange-200 transition"
              >
                Get Started
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
