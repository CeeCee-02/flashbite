"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { authService, RegisterPayload } from "../services/auth";
import { useAuthStore } from "../store/authStore";
import { Lock, Mail, User, Phone, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";

interface AuthFormProps {
  type: "login" | "register";
  role: "customer" | "restaurant" | "rider";
}

export default function AuthForm({ type, role }: AuthFormProps) {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  const [formData, setFormData] = useState({
    email: "",
    full_name: "",
    phone: "",
    password: "",
    password_confirm: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const roleTitles = {
    customer: "Foodie Account",
    restaurant: "Restaurant Partner",
    rider: "Delivery Fleet",
  };

  const roleBadgeColors = {
    customer: "bg-orange-100 text-orange-700 border-orange-200",
    restaurant: "bg-amber-100 text-amber-800 border-amber-200",
    rider: "bg-emerald-100 text-emerald-800 border-emerald-200",
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccessMsg(null);

    try {
      if (type === "register") {
        if (formData.password !== formData.password_confirm) {
          setError("Passwords do not match.");
          setLoading(false);
          return;
        }

        const payload: RegisterPayload = {
          email: formData.email,
          full_name: formData.full_name,
          phone: formData.phone,
          role,
          password: formData.password,
          password_confirm: formData.password_confirm,
        };

        const res = await authService.register(payload);
        setSuccessMsg(res.message || "Account created! Please check your email to verify your account.");
      } else {
        const res = await authService.login({
          email: formData.email,
          password: formData.password,
        });

        setAuth(res.user, res.access, res.refresh);

        // Redirect based on role
        if (res.user.role === "restaurant") {
          router.push("/restaurant/dashboard");
        } else if (res.user.role === "rider") {
          router.push("/rider/dashboard");
        } else {
          router.push("/customer/dashboard");
        }
      }
    } catch (err: any) {
      const msg =
        err.response?.data?.message ||
        err.response?.data?.error ||
        "An unexpected error occurred. Please check your credentials and try again.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-100 p-8">
      {/* Header */}
      <div className="text-center mb-6">
        <span
          className={`inline-block text-xs font-semibold px-3 py-1 rounded-full border mb-3 ${roleBadgeColors[role]}`}
        >
          {roleTitles[role]}
        </span>
        <h2 className="text-2xl font-black text-slate-900">
          {type === "login" ? "Welcome back to Flashbite" : "Create your Flashbite account"}
        </h2>
        <p className="text-sm text-slate-500 mt-1">
          {type === "login"
            ? "Sign in to access your portal and orders"
            : "Get started in less than 2 minutes"}
        </p>
      </div>

      {/* Alerts */}
      {error && (
        <div className="mb-4 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-sm flex items-start gap-2">
          <AlertCircle className="w-5 h-5 shrink-0 text-rose-500 mt-0.5" />
          <div>{error}</div>
        </div>
      )}

      {successMsg && (
        <div className="mb-4 p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm flex items-start gap-2">
          <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-500 mt-0.5" />
          <div>{successMsg}</div>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {type === "register" && (
          <>
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Full Name
              </label>
              <div className="relative">
                <User className="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  value={formData.full_name}
                  onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                  placeholder="e.g. Chinedu Okafor"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Phone Number
              </label>
              <div className="relative">
                <Phone className="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  placeholder="e.g. 08012345678"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
                />
              </div>
            </div>
          </>
        )}

        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
            Email Address
          </label>
          <div className="relative">
            <Mail className="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder="you@example.com"
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
            Password
          </label>
          <div className="relative">
            <Lock className="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder="••••••••"
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
            />
          </div>
        </div>

        {type === "register" && (
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
              Confirm Password
            </label>
            <div className="relative">
              <Lock className="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                value={formData.password_confirm}
                onChange={(e) => setFormData({ ...formData, password_confirm: e.target.value })}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
              />
            </div>
          </div>
        )}

        {type === "login" && (
          <div className="flex justify-end">
            <Link
              href="/reset-password"
              className="text-xs font-semibold text-orange-600 hover:text-orange-700 transition"
            >
              Forgot password?
            </Link>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 px-4 bg-orange-600 hover:bg-orange-700 text-white font-bold rounded-xl shadow-md shadow-orange-200 transition flex items-center justify-center gap-2 disabled:opacity-50 text-sm mt-2"
        >
          {loading ? (
            "Please wait..."
          ) : (
            <>
              {type === "login" ? "Sign In" : "Create Account"}
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </form>

      {/* Switch Form Type */}
      <div className="mt-6 text-center text-xs text-slate-500">
        {type === "login" ? (
          <>
            Don't have an account?{" "}
            <Link
              href={`/${role}/register`}
              className="font-bold text-orange-600 hover:text-orange-700 transition"
            >
              Sign up as {role}
            </Link>
          </>
        ) : (
          <>
            Already have an account?{" "}
            <Link
              href={`/${role}/login`}
              className="font-bold text-orange-600 hover:text-orange-700 transition"
            >
              Sign in
            </Link>
          </>
        )}
      </div>
    </div>
  );
}
