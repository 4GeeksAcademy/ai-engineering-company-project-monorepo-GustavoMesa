/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'http://services:8000',
  },
};

module.exports = nextConfig;