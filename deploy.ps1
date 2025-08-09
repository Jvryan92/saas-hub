$ErrorActionPreference = "Stop"
Write-Host "Starting deploy..." -ForegroundColor Cyan

# Pull env from Vercel (if project is already linked), else continue silently
try { vercel pull --yes --environment=production --token $env:VERCEL_TOKEN | Out-Null } catch { }

# Link if needed (suppresses prompts if VERCEL_TOKEN provided)
try {
  vercel link --yes --project $env:VERCEL_PROJECT --token $env:VERCEL_TOKEN | Out-Null
} catch { }

# Deploy (static site served from public via vercel.json)
vercel deploy --prebuilt --prod --token $env:VERCEL_TOKEN
