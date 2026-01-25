# PowerShell script to generate nginx.conf from environment variables
# Usage: .\generate_nginx_config.ps1
# 
# Environment variables to set before running:
#   NGINX_DOMAIN         - Domain name(s) for nginx (e.g., "api.example.com")
#   NGINX_CERT_PATH      - Path to SSL certificate fullchain.pem (e.g., "C:/certs/fullchain.pem")
#   NGINX_KEY_PATH       - Path to SSL private key privkey.pem (e.g., "C:/certs/privkey.pem")
#   FRONTEND_ROOT        - Path to frontend build directory (e.g., "d:/SoftwareDevelopement/BlobSim/web-ui/dist")
#   BACKEND_HOST         - Backend host (optional, default: 127.0.0.1)
#   BACKEND_PORT         - Backend port (optional, default: 8000)

param(
    [string]$TemplateFile = "nginx.conf.template",
    [string]$OutputFile = "C:\nginx\conf\nginx.conf"
)

# Set defaults for optional env vars
if (-not $env:BACKEND_HOST) {
    $env:BACKEND_HOST = "127.0.0.1"
}
if (-not $env:BACKEND_PORT) {
    $env:BACKEND_PORT = "8000"
}

# Extract primary domain from NGINX_DOMAIN (first domain if multiple)
$domains = $env:NGINX_DOMAIN -split '\s+'
$env:NGINX_DOMAIN_PRIMARY = $domains[0]

# Validate required environment variables
$requiredVars = @("NGINX_DOMAIN", "NGINX_CERT_PATH", "NGINX_KEY_PATH", "FRONTEND_ROOT")
foreach ($var in $requiredVars) {
    if (-not (Get-Item -Path "env:$var" -ErrorAction SilentlyContinue)) {
        Write-Error "ERROR: Environment variable '$var' is not set"
        Write-Host ""
        Write-Host "Required environment variables:"
        Write-Host "  `$env:NGINX_DOMAIN = '<domain or space-separated domains>'"
        Write-Host "  `$env:NGINX_CERT_PATH = '<path to fullchain.pem>'"
        Write-Host "  `$env:NGINX_KEY_PATH = '<path to privkey.pem>'"
        Write-Host "  `$env:FRONTEND_ROOT = '<path to web-ui/dist or build directory>'"
        Write-Host ""
        Write-Host "Optional environment variables:"
        Write-Host "  `$env:BACKEND_HOST (default: 127.0.0.1)"
        Write-Host "  `$env:BACKEND_PORT (default: 8000)"
        exit 1
    }
}

# Read template file
if (-not (Test-Path $TemplateFile)) {
    Write-Error "Template file not found: $TemplateFile"
    exit 1
}

Write-Host "Reading template from: $TemplateFile"
$content = Get-Content -Path $TemplateFile -Raw

# Replace placeholders with environment variable values
Write-Host "Substituting environment variables..."
Write-Host "  NGINX_DOMAIN = $env:NGINX_DOMAIN"
Write-Host "  NGINX_DOMAIN_PRIMARY = $env:NGINX_DOMAIN_PRIMARY"
Write-Host "  NGINX_CERT_PATH = $env:NGINX_CERT_PATH"
Write-Host "  NGINX_KEY_PATH = $env:NGINX_KEY_PATH"
Write-Host "  FRONTEND_ROOT = $env:FRONTEND_ROOT"
Write-Host "  BACKEND_HOST = $env:BACKEND_HOST"
Write-Host "  BACKEND_PORT = $env:BACKEND_PORT"

$content = $content.Replace('${NGINX_DOMAIN}', $env:NGINX_DOMAIN)
$content = $content.Replace('${NGINX_DOMAIN_PRIMARY}', $env:NGINX_DOMAIN_PRIMARY)
$content = $content.Replace('${NGINX_CERT_PATH}', $env:NGINX_CERT_PATH)
$content = $content.Replace('${NGINX_KEY_PATH}', $env:NGINX_KEY_PATH)
$content = $content.Replace('${FRONTEND_ROOT}', $env:FRONTEND_ROOT)
$content = $content.Replace('${BACKEND_HOST}', $env:BACKEND_HOST)
$content = $content.Replace('${BACKEND_PORT}', $env:BACKEND_PORT)

# Ensure output directory exists
$outputDir = Split-Path -Path $OutputFile
if (-not (Test-Path $outputDir)) {
    Write-Host "Creating output directory: $outputDir"
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Write output file
Write-Host "Writing generated config to: $OutputFile"
Set-Content -Path $OutputFile -Value $content

Write-Host ""
Write-Host "SUCCESS! nginx.conf generated from environment variables"
Write-Host ""
