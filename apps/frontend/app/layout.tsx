import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Todo App - Manage Your Tasks",
  description: "Full-stack todo application with Next.js and FastAPI. Create, update, and manage your tasks efficiently.",
  keywords: ["todo", "task management", "productivity", "next.js", "fastapi"],
  authors: [{ name: "Todo App Team" }],
  viewport: "width=device-width, initial-scale=1",
  themeColor: "#3B82F6",
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/icon.svg", type: "image/svg+xml" },
    ],
    apple: "/apple-touch-icon.png",
  },
  manifest: "/manifest.json",
  openGraph: {
    title: "Todo App - Manage Your Tasks",
    description: "Full-stack todo application with Next.js and FastAPI",
    type: "website",
    locale: "en_US",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
