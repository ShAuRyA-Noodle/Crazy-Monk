/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      // taste-skill: NEVER Inter for premium/creative. Use Geist + Cabinet Grotesk.
      fontFamily: {
        display: ["Cabinet Grotesk", "Satoshi", "system-ui", "sans-serif"],
        sans: ["Geist", "system-ui", "sans-serif"],
        mono: ["Geist Mono", "ui-monospace", "monospace"],
      },
      colors: {
        // taste-skill: neutral bases (Zinc/Slate) with high-contrast singular accents.
        // No purple/blue gradients, no AI-tells.
        ink: {
          50: "#FAFAFA",
          100: "#F4F4F5",
          200: "#E4E4E7",
          300: "#D4D4D8",
          400: "#A1A1AA",
          500: "#71717A",
          600: "#52525B",
          700: "#3F3F46",
          800: "#27272A",
          900: "#18181B",
          950: "#09090B",
        },
        accent: {
          DEFAULT: "#FF5A1F",
          50: "#FFF1EB",
          100: "#FFE3D6",
          200: "#FFC2A8",
          300: "#FFA079",
          400: "#FF7E4B",
          500: "#FF5A1F",
          600: "#E63E00",
          700: "#B23000",
          800: "#7E2200",
          900: "#4A1400",
        },
        success: { DEFAULT: "#16A34A" },
        warning: { DEFAULT: "#EAB308" },
        danger: { DEFAULT: "#DC2626" },
      },
      borderRadius: {
        bento: "2.5rem",
      },
      boxShadow: {
        diffusion: "0 20px 40px -15px rgba(0,0,0,0.05)",
        bento: "0 1px 0 0 rgba(255,255,255,0.04) inset, 0 0 0 1px rgba(0,0,0,0.04), 0 30px 60px -30px rgba(0,0,0,0.12)",
      },
      animation: {
        "breathe": "breathe 2.4s ease-in-out infinite",
        "shimmer": "shimmer 2.2s linear infinite",
      },
      keyframes: {
        breathe: {
          "0%, 100%": { opacity: "0.45" },
          "50%": { opacity: "1" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
    },
  },
  plugins: [],
};
