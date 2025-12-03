/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_GOOGLE_CLIENT_ID: string
  readonly VITE_GOOGLE_API_KEY: string
  readonly VITE_VERCEL_ACCESS_TOKEN: string
  readonly VITE_CLOUDFLARE_API_TOKEN: string
  readonly VITE_CLOUDFLARE_ACCOUNT_ID: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}