"use client";

import { useAuthStore } from "../../../store/authStore";
import { Utensils, Plus, CheckCircle, Store } from "lucide-react";

export default function RestaurantDashboardPage() {
  const { user } = useAuthStore();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900">
            Restaurant Partner Portal 🍽️
          </h1>
          <p className="text-slate-600 text-sm mt-1">
            Owner: <span className="font-semibold">{user?.full_name}</span> ({user?.email})
          </p>
        </div>
        <span className="px-3 py-1 rounded-full bg-amber-100 border border-amber-200 text-amber-800 text-xs font-bold">
          Milestone 1 Verified
        </span>
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-8 text-center max-w-xl mx-auto my-12">
        <div className="w-12 h-12 bg-amber-600 text-white rounded-2xl flex items-center justify-center mx-auto mb-4">
          <Store className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Ready for Milestone 2!</h2>
        <p className="text-sm text-slate-600 mt-2">
          Milestone 2 (Restaurant Management) will enable creating your store profile, uploading banners/logos to Supabase Storage, and managing your food menu CRUD.
        </p>
      </div>
    </div>
  );
}
