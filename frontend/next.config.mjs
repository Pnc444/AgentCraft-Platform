/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    // Proxy browser API calls through Next so remote devices don't resolve localhost to themselves.
    const internalApiUrl = process.env.INTERNAL_API_URL || "http://localhost:8000";
    return [
      {
        source: "/api/v1/:path*",
        destination: `${internalApiUrl}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;
