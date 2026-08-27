import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#FFF5F2",
          100: "#FFE8E1",
          200: "#FFD1C4",
          500: "#FF5722", // Primary Flashbite Orange
          600: "#E64A19",
          700: "#D84315",
          900: "#26130D",
        },
        dark: {
          900: "#0F172A",
          800: "#1E293B",
          700: "#334155",
        }
      },
    },
  },
  plugins: [],
};
export default config;
