/** @type {import('next').NextConfig} */
const API_BASE = process.env.API_BASE;
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${API_BASE}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
