const inventoryApiUrl =
  process.env.INVENTORY_API_URL ?? "http://localhost:8000/api/v1/inventory";

/** @type {import('next').NextConfig} */
const nextConfig = {
  poweredByHeader: false,
  turbopack: {
    root: process.cwd(),
  },
  async rewrites() {
    return [
      {
        source: "/api/inventory/:path*",
        destination: `${inventoryApiUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
