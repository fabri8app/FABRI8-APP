import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Fabri8 Agent Builder",
  description: "AI Powered Web Builder Team",
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
