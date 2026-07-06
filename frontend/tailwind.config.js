/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          main: "var(--primary-main)",
          soft: "var(--primary-soft)",
          muted: "var(--primary-muted)",
        },
        surface: {
          app: "var(--surface-app)",
          card: "var(--surface-card)",
          border: "var(--surface-border)",
          muted: "var(--surface-muted)",
        },
        text: {
          base: "var(--text-base)",
          muted: "var(--text-muted)",
          inverse: "var(--text-inverse)",
        },
        status: {
          success: "var(--status-success)",
          warning: "var(--status-warning)",
          error: "var(--status-error)",
          info: "var(--status-info)",
        }
      },
      boxShadow: {
        soft: "var(--shadow-soft)",
      },
    },
  },
  plugins: [],
}
