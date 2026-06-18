import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Overpass, Overpass_Mono } from "next/font/google";
import { Providers } from "./providers";
import "./globals.css";

const overpass = Overpass({
  subsets: ["latin"],
  weight: ["300", "400", "600"],
  variable: "--font-overpass",
  display: "swap",
});

const overpassMono = Overpass_Mono({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-overpass-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Citi | Ops Risk Reporting",
  description: "CopilotKit A2UI reporting analyst workspace for ADK agents",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en" className={`${overpass.variable} ${overpassMono.variable}`}>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}