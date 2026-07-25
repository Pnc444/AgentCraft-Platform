/** @type {import('next').NextConfig} */
const nextConfig = {
  // Django API URLs end in a trailing slash; without this Next strips it
  // (308 redirect) before the rewrite reaches the backend.
  skipTrailingSlashRedirect: true,
  async rewrites() {
    // Proxy browser API calls through Next so remote devices don't resolve localhost to themselves.
    const internalApiUrl = process.env.INTERNAL_API_URL || "http://localhost:8001";
    return [
      {
        source: "/api/v1/:path*",
        destination: `${internalApiUrl}/api/v1/:path*`,
      },
      {
        source: "/media/:path*",
        destination: `${internalApiUrl}/media/:path*`,
      },
    ];
  },
};

export default nextConfig;
