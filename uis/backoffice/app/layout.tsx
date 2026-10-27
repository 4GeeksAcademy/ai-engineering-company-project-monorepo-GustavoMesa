import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Inventario | Brasaland Backoffice",
  description: "Gestión interna de inventario de Brasaland.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
