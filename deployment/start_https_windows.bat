@echo off
REM Windows startup script for BlobSim with HTTPS
REM This script generates nginx.conf from env vars, then starts uvicorn + Nginx
REM Nginx serves both the frontend (static SPA) and proxies API calls to the backend
REM 
REM Prerequisites:
REM   - Python environment with FastAPI/uvicorn installed
REM   - Nginx installed at C:\nginx
REM   - Frontend built to web-ui\dist or similar
REM   - SSL certificates in C:\certs (from win-acme)
REM 
REM Required Environment Variables:
REM   NGINX_DOMAIN         - Domain name(s) for nginx (e.g., "api.example.com")
REM   NGINX_CERT_PATH      - Path to fullchain.pem (e.g., "C:/certs/fullchain.pem")
REM   NGINX_KEY_PATH       - Path to privkey.pem (e.g., "C:/certs/privkey.pem")
REM   FRONTEND_ROOT        - Path to frontend build dir (e.g., "d:/SoftwareDevelopement/BlobSim/web-ui/dist")
REM 
REM Optional Environment Variables:
REM   BACKEND_HOST         - Backend host (default: 127.0.0.1)
REM   BACKEND_PORT         - Backend port (default: 8000)
REM   ORIGIN_URL           - CORS origin URL (e.g., "https://api.example.com")

setlocal enabledelayedexpansion

echo.
echo ========================================
echo BlobSim (Frontend + Backend) + HTTPS
echo ========================================
echo.

REM Check if NGINX_DOMAIN is set
if not defined NGINX_DOMAIN (
    echo ERROR: NGINX_DOMAIN environment variable not set
    echo.
    echo Usage: Set environment variables before running this script:
    echo   set NGINX_DOMAIN=api.example.com
    echo   set NGINX_CERT_PATH=C:/certs/fullchain.pem
    echo   set NGINX_KEY_PATH=C:/certs/privkey.pem
    echo   set FRONTEND_ROOT=d:/SoftwareDevelopement/BlobSim/web-ui/dist
    echo   start_https_windows.bat
    echo.
    exit /b 1
)

if not defined FRONTEND_ROOT (
    echo ERROR: FRONTEND_ROOT environment variable not set
    echo Please set FRONTEND_ROOT to your frontend build directory
    echo.
    exit /b 1
)

REM Set defaults for optional environment variables
if not defined BACKEND_HOST (
    set BACKEND_HOST=127.0.0.1
)
if not defined BACKEND_PORT (
    set BACKEND_PORT=8000
)

REM Set derived variables
set ORIGIN_URL=https://%NGINX_DOMAIN%

REM Verify environment
echo [1/4] Checking environment...
if not exist "C:\nginx\nginx.exe" (
    echo ERROR: Nginx not found at C:\nginx\nginx.exe
    echo Please install Nginx for Windows from https://nginx.org/
    exit /b 1
)

if not exist "!NGINX_CERT_PATH!" (
    echo ERROR: Certificate not found at !NGINX_CERT_PATH!
    echo Please run win-acme to provision Let's Encrypt certificates
    exit /b 1
)

echo [OK] Nginx and certificates found
echo.

REM Generate nginx.conf from environment variables
echo [2/4] Generating nginx.conf from environment variables...
powershell -NoProfile -ExecutionPolicy Bypass -File "!~dp0generate_nginx_config.ps1"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to generate nginx.conf
    exit /b 1
)
echo.

REM Start uvicorn backend on localhost:8000
echo [3/4] Starting FastAPI backend (uvicorn) on !BACKEND_HOST!:!BACKEND_PORT!...
set PYTHONUNBUFFERED=1

REM Create a separate window for uvicorn so it doesn't block Nginx startup
REM --proxy-headers: Trust X-Forwarded-* headers from nginx
REM --forwarded-allow-ips: Allow proxy headers from localhost (nginx)
REM Pass ORIGIN_URL environment variable to the new process explicitly
start "BlobSim Backend" cmd /k "cd /d d:\SoftwareDevelopement\BlobSim && set ORIGIN_URL=!ORIGIN_URL! && uvicorn main:app --host !BACKEND_HOST! --port !BACKEND_PORT! --proxy-headers --forwarded-allow-ips 127.0.0.1"

REM Give uvicorn a moment to start
timeout /t 2 /nobreak

REM Start Nginx
echo [4/4] Starting Nginx (HTTPS reverse proxy)...
cd /d C:\nginx

REM Verify Nginx config syntax
nginx.exe -t
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Nginx configuration is invalid. Check C:\nginx\conf\nginx.conf
    exit /b 1
)

REM Start Nginx
start "Nginx" nginx.exe

echo.
echo ========================================
echo SUCCESS! Services are starting...
echo ========================================
echo.
echo Domain:         !NGINX_DOMAIN!
echo Frontend Root:  !FRONTEND_ROOT!
echo Backend:        http://!BACKEND_HOST!:!BACKEND_PORT!  (internal only)
echo.
echo Frontend:       https://!NGINX_DOMAIN!/
echo API:            https://!NGINX_DOMAIN!/api/
echo Docs:           https://!NGINX_DOMAIN!/docs
echo.
echo Open your browser to https://!NGINX_DOMAIN!
echo.
echo Press Ctrl+C in any terminal to stop services.
echo.

endlocal
