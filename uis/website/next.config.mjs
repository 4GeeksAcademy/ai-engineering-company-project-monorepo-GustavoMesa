/** @type {import('next').NextConfig} */
const nextConfig = {
  poweredByHeader: false,
  output: "standalone",
  env: {
    BACKEND_URL: process.env.BACKEND_URL || "http://services:8000",
  },
  allowedDevOrigins: ["161.35.78.162", "localhost", "127.0.0.1"],
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;