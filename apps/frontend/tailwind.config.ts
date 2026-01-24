import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Golden/Amber Theme
        primary: {
          DEFAULT: "#FDB813",
          dark: "#F5A623",
          light: "#FDD85D",
        },
        secondary: {
          DEFAULT: "#1A1A1A",
          light: "#333333",
        },
        // Text Colors
        text: {
          primary: "#1A1A1A",
          secondary: "#666666",
          tertiary: "#999999",
          disabled: "#CCCCCC",
        },
        // Background Colors
        background: {
          DEFAULT: "#FFFFFF",
          subtle: "#FAFAFA",
          muted: "#F5F5F5",
        },
        // Border Colors
        border: {
          DEFAULT: "#EAEAEA",
          light: "#F0F0F0",
          dark: "#D0D0D0",
        },
        // Status Colors
        success: "#10B981",
        warning: "#F59E0B",
        danger: "#EF4444",
        // Priority Colors (Todoist-style)
        priority: {
          1: "#D1453B", // Red
          2: "#FF9933", // Orange
          3: "#5297FF", // Blue
          4: "#CCCCCC", // Gray
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Oxygen",
          "Ubuntu",
          "Cantarell",
          "Fira Sans",
          "Droid Sans",
          "Helvetica Neue",
          "sans-serif",
        ],
      },
      fontSize: {
        xs: "12px",
        sm: "13px",
        base: "14px",
        lg: "16px",
        xl: "18px",
        "2xl": "24px",
        "3xl": "32px",
      },
      spacing: {
        sidebar: "264px",
      },
    },
  },
  plugins: [],
};
export default config;
