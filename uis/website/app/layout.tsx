import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Brasaland | Fuego, sabor y encuentros",
  description:
    "Brasaland: cocina a la brasa nacida en Medellín, hecha para compartir.",
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
