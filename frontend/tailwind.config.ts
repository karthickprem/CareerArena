import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          '"Segoe UI"',
          "Roboto",
          '"Helvetica Neue"',
          "Arial",
          "sans-serif",
        ],
        display: [
          '"Plus Jakarta Sans"',
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
        ],
        mono: [
          '"JetBrains Mono"',
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "monospace",
        ],
      },
      colors: {
        ca: {
          bg: "var(--background)",
          "bg-secondary": "var(--background-secondary)",
          fg: "var(--foreground)",
          "fg-secondary": "var(--foreground-secondary)",
          "fg-muted": "var(--foreground-muted)",
          accent: "var(--accent)",
          "accent-hover": "var(--accent-hover)",
          "accent-light": "var(--accent-light)",
          border: "var(--border)",
          card: "var(--card)",
          success: "var(--success)",
          warning: "var(--warning)",
          danger: "var(--danger)",
        },
      },
      borderRadius: {
        "ca-sm": "var(--radius-sm)",
        "ca-md": "var(--radius-md)",
        "ca-lg": "var(--radius-lg)",
        "ca-xl": "var(--radius-xl)",
        "ca-2xl": "var(--radius-2xl)",
      },
      boxShadow: {
        "ca-sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        "ca-md": "0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05)",
        "ca-lg": "0 10px 15px -3px rgb(0 0 0 / 0.05), 0 4px 6px -4px rgb(0 0 0 / 0.05)",
      },
    },
  },
  plugins: [],
};
export default config;
