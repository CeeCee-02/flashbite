"use client";

import { useAuthStore } from "../../../store/authStore";
import { ShoppingBag, MapPin, CheckCircle, Clock } from "lucide-react";

export default function CustomerDashboardPage() {
  const { user } = useAuthStore();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-8">
        <h1 className="text-2xl font-black text-slate-900">
          Welcome back, {user?.full_name || "Foodie"}! 👋
        </h1>
        <p className="text-slate-600 text-sm mt-1">
          Explore restaurants around you and place your next Flashbite order.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-orange-50 border border-orange-200 rounded-2xl p-6">
          <div className="w-10 h-10 rounded-xl bg-orange-600 text-white flex items-center justify-center mb-4">
            <ShoppingBag className="w-5 h-5" />
          </div>
          <h2 className="font-bold text-slate-900">Milestone 1 Active</h2>
          <p className="text-xs text-slate-600 mt-1">
            Authentication is ready. Restaurant listing and food catalog arrive in Milestone 2!
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-4">
            <CheckCircle className="w-5 h-5" />
          </div>
          <h2 className="font-bold text-slate-900">Verified Account</h2>
          <p className="text-xs text-slate-600 mt-1">
            Role: <span className="font-semibold text-slate-800">{user?.role}</span> ({user?.email})
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6">
          <div className="w-10 h-10 rounded-xl bg-slate-100 text-slate-600 flex items-center justify-center mb-4">
            <Clock className="w-5 h-5" />
          </div>
          <h2 className="font-bold text-slate-900">Next Milestone</h2>
          <p className="text-xs text-slate-600 mt-1">
            Milestone 2 will add Restaurant profile creation, PostGIS geo-location & menu CRUD.
          </p>
        </div>
      </div>
    </div>
  );
}
