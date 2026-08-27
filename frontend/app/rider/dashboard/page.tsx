"use client";

import { useAuthStore } from "../../../store/authStore";
import { Bike, Navigation, ShieldCheck } from "lucide-react";

export default function RiderDashboardPage() {
  const { user } = useAuthStore();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900">
            Rider Fleet Portal 🚴
          </h1>
          <p className="text-slate-600 text-sm mt-1">
            Rider: <span className="font-semibold">{user?.full_name}</span> ({user?.email})
          </p>
        </div>
        <span className="px-3 py-1 rounded-full bg-emerald-100 border border-emerald-200 text-emerald-800 text-xs font-bold">
          Milestone 1 Verified
        </span>
      </div>

      <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-8 text-center max-w-xl mx-auto my-12">
        <div className="w-12 h-12 bg-emerald-600 text-white rounded-2xl flex items-center justify-center mx-auto mb-4">
          <Navigation className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Ready for Milestone 5 & 6!</h2>
        <p className="text-sm text-slate-600 mt-2">
          Milestone 5 will add Rider Document Verification & Order Dispatching. Milestone 6 will add 15-30s throttled live GPS tracking over WebSockets!
        </p>
      </div>
    </div>
  );
}
