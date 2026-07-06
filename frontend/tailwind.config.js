/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          main: "#6366f1",
          soft: "#e0e7ff",
        },
        surface: {
          app: "#f8fafc",
          card: "#ffffff",
          border: "#e2e8f0",
        },
        status: {
          success: "#10b981",
          warning: "#f59e0b",
          error: "#ef4444",
          info: "#3b82f6",
        }
      }
    },
  },
  plugins: [],
}
