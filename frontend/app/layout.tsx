import type { Metadata } from "next";
import "./globals.css";
import Navbar from "../components/Navbar";

export const metadata: Metadata = {
  title: "FLASHBITE — Hyper-Fast Food Delivery in Nigeria",
  description: "Order delicious meals from your favorite local Nigerian restaurants and get them delivered hot & fresh to your doorstep.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 min-h-screen flex flex-col antialiased">
        <Navbar />
        <main className="flex-1">{children}</main>
        <footer className="bg-slate-900 text-slate-400 border-t border-slate-800 py-10">
          <div className="max-w-7xl mx-auto px-4 text-center text-xs space-y-2">
            <p className="font-bold text-white text-sm">FLASHBITE Platform</p>
            <p>Built for Nigeria · Powered by Django, Next.js & Supabase</p>
            <p className="text-slate-500">© {new Date().getFullYear()} FLASHBITE. All rights reserved.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
