/** @type {import('next').NextConfig} */
const nextConfig = {

  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'content.r9cdn.net',
        pathname: '/rimg/**',
      },
    ],
  },
};

module.exports = nextConfig;
