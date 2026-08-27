"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { authService } from "../../services/auth";
import { CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");

  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) {
      setLoading(false);
      setMessage("Verification token is missing.");
      return;
    }

    authService
      .verifyEmail(token)
      .then((res) => {
        setSuccess(true);
        setMessage(res.message || "Email verified successfully!");
      })
      .catch((err) => {
        setSuccess(false);
        setMessage(
          err.response?.data?.message ||
            "Verification link is invalid or has expired."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token]);

  return (
    <div className="w-full max-w-md bg-white rounded-2xl shadow-xl border border-slate-100 p-8 text-center">
      {loading ? (
        <div className="py-8 flex flex-col items-center gap-3">
          <Loader2 className="w-10 h-10 text-orange-600 animate-spin" />
          <p className="text-sm font-semibold text-slate-600">Verifying your email address...</p>
        </div>
      ) : success ? (
        <div className="py-6 space-y-4">
          <div className="w-14 h-14 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
            <CheckCircle2 className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-black text-slate-900">Email Verified!</h2>
          <p className="text-sm text-slate-600">{message}</p>
          <div className="pt-4">
            <Link
              href="/customer/login"
              className="inline-block w-full py-3 px-4 bg-orange-600 hover:bg-orange-700 text-white font-bold rounded-xl shadow-md shadow-orange-200 transition text-sm"
            >
              Sign In to Your Account
            </Link>
          </div>
        </div>
      ) : (
        <div className="py-6 space-y-4">
          <div className="w-14 h-14 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto">
            <AlertCircle className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-black text-slate-900">Verification Failed</h2>
          <p className="text-sm text-slate-600">{message}</p>
          <div className="pt-4">
            <Link
              href="/customer/login"
              className="inline-block w-full py-3 px-4 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl transition text-sm"
            >
              Go to Sign In
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <div className="py-12 flex justify-center items-center px-4 min-h-[calc(100vh-4rem)]">
      <Suspense fallback={<div>Loading...</div>}>
        <VerifyEmailContent />
      </Suspense>
    </div>
  );
}
