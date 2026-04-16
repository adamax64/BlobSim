# Load environment variables from .env file
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = Join-Path $scriptDir ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value)
        }
    }
}

# Set defaults if not set
if (-not $env:SERVER_NAME) { $env:SERVER_NAME = "localhost" }
if (-not $env:ROOT_PATH) { $env:ROOT_PATH = Join-Path $scriptDir "dist" }

# Preprocess nginx config
$configTemplate = Join-Path $scriptDir "nginx.conf"
$configOutput = Join-Path $scriptDir "nginx_processed.conf"

(Get-Content $configTemplate) -replace '\$\{([^}]+)\}', {
    param($match)
    $varName = $match.Groups[1].Value
    [Environment]::GetEnvironmentVariable($varName) ?? $match.Value
} | Set-Content $configOutput

# Run nginx with processed config
# Note: Update the nginx path if it's not in your PATH
& $env:NGINX_PATH\nginx.exe -c $configOutput