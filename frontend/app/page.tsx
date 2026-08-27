import Link from "next/link";
import { Utensils, Bike, ShoppingBag, ShieldCheck, Zap, MapPin } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="relative overflow-hidden">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-orange-50/50 via-white to-slate-50 py-20 lg:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-orange-100 border border-orange-200 text-orange-700 text-xs font-bold uppercase tracking-wider mb-6">
            <Zap className="w-4 h-4 fill-orange-500 text-orange-500" />
            Nigeria's Bootstrap MVP Delivery Platform
          </div>

          <h1 className="text-4xl sm:text-6xl font-black text-slate-900 tracking-tight max-w-4xl mx-auto leading-tight">
            Delicious food from your favorite spots, <span className="text-orange-600">delivered at flash speed.</span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto">
            Order Jollof, Suya, Amala, Burgers & drinks straight to your home or office. Real-time GPS tracking included.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/customer/register"
              className="px-8 py-4 rounded-xl bg-orange-600 hover:bg-orange-700 text-white font-bold text-base shadow-lg shadow-orange-200 transition"
            >
              Order Food Now
            </Link>
            <Link
              href="/restaurant/register"
              className="px-8 py-4 rounded-xl bg-white hover:bg-slate-50 text-slate-800 font-bold text-base border border-slate-200 shadow-sm transition"
            >
              Partner as Restaurant
            </Link>
          </div>
        </div>
      </section>

      {/* Portal Selection Cards */}
      <section className="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-black text-center text-slate-900 mb-10">Choose Your Flashbite Portal</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Customer Card */}
          <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center mb-6">
                <ShoppingBag className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-2">Foodie Customer Portal</h3>
              <p className="text-sm text-slate-600 mb-6">
                Browse nearby restaurants, build your cart, checkout with Paystack, and track your rider in real time.
              </p>
            </div>
            <div className="flex gap-2">
              <Link
                href="/customer/login"
                className="flex-1 text-center py-2.5 rounded-lg bg-orange-600 text-white font-semibold text-sm hover:bg-orange-700 transition"
              >
                Customer Login
              </Link>
              <Link
                href="/customer/register"
                className="flex-1 text-center py-2.5 rounded-lg border border-slate-200 text-slate-700 font-semibold text-sm hover:bg-slate-50 transition"
              >
                Register
              </Link>
            </div>
          </div>

          {/* Restaurant Card */}
          <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center mb-6">
                <Utensils className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-2">Restaurant Portal</h3>
              <p className="text-sm text-slate-600 mb-6">
                Manage your menu, set dish prices, upload food images, and process live orders from customers.
              </p>
            </div>
            <div className="flex gap-2">
              <Link
                href="/restaurant/login"
                className="flex-1 text-center py-2.5 rounded-lg bg-amber-600 text-white font-semibold text-sm hover:bg-amber-700 transition"
              >
                Vendor Login
              </Link>
              <Link
                href="/restaurant/register"
                className="flex-1 text-center py-2.5 rounded-lg border border-slate-200 text-slate-700 font-semibold text-sm hover:bg-slate-50 transition"
              >
                Register
              </Link>
            </div>
          </div>

          {/* Rider Card */}
          <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-6">
                <Bike className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-2">Rider Fleet Portal</h3>
              <p className="text-sm text-slate-600 mb-6">
                Accept nearby ready orders, stream your live GPS location, and complete deliveries to earn.
              </p>
            </div>
            <div className="flex gap-2">
              <Link
                href="/rider/login"
                className="flex-1 text-center py-2.5 rounded-lg bg-emerald-600 text-white font-semibold text-sm hover:bg-emerald-700 transition"
              >
                Rider Login
              </Link>
              <Link
                href="/rider/register"
                className="flex-1 text-center py-2.5 rounded-lg border border-slate-200 text-slate-700 font-semibold text-sm hover:bg-slate-50 transition"
              >
                Register
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
